var i2c = require('i2c');
var fs  = require('fs');

'use strict';

/* Version of the API */
var APIVERSION = 0.3;

/* For at least mopi firmware vX.YY... */
var FIRMMAJ  = 3;
var FIRMMINR = 5;

/* Number of times to retry a failed I2C read/write to the MoPi */
var MAXTRIES = 3;

function get_rpi_revision (callback) { /* Logic taken from https://pypi.python.org/pypi/RPi.GPIO */
    fs.readFile('/proc/cpuinfo', function (err, data) {
        if (err) return callback();

        var rpi_found = false, revision = null;

        data.toString().split("\n").forEach(function(line){
            if (line.match(/^Hardware\s*:\s*BCM2708$/)) rpi_found = true;
            if (line.match(/^Revision\s*:.*[0-9a-f]{4}$/)) revision = line.replace(/^.+([0-9a-f]{4})$/,'$1');
        });

        revision = !rpi_found || revision === null ? null
             : revision.match('^000[23]$')        ? 1 /* Revision 1 */
             : revision.match('^000[456789def]$') ? 2 /* Revision 2 */
             : revision === '0011'                ? 0 /* Compute module */
             : 3                                      /* assume B+ (0010) */

        revision === null ? callback() : callback(revision);
    });
}

function guessI2C (callback) {
    /* Rev2 of RPi switched the i2c address, so return the right one for the board we have */
    get_rpi_revision(function(rev){
        callback(rev == 1 ? 0 : 1);
    });
}

function mopiapi (i2cbus) {
    this._device = 0xb;
    if (typeof(i2cbus) === 'number') this._i2cbus = i2cbus;
}

mopiapi.prototype = {

    connect: function (callback) {

        /* If we weren't given a bus, guess which one to use */

            if (!('_i2cbus' in this)) return guessI2C(function(ic2bus){
                this._i2cbus = ic2bus;
                this.connect(callback);
            }.bind(this));

        this._wire = new i2c(this._device, { device: '/dev/i2c-' + this._i2cbus });

        this.getFirmwareVersion(function(err, version){
            if (!err && (version[0] != FIRMMAJ || version[1] < FIRMMINR)) {
                err = 'Expected at least MoPi firmware version ' + FIRMMAJ + '.' + FIRMMINR
                    + ', got ' + version[0] + '.' + version[1] + ' instead.';
            }
            if (callback) callback(err);
        }.bind(this));
    },

    getStatus: function (callback) {
        this.getFirmwareVersion(function (err, version){
            if (err) return callback(err);

            this.readWord(0, function (err, word){
                if (!err && version[0] === 3 && version[1] > 9) word = word ^ (1 << 6);
                callback(err, word);
            });
        }.bind(this));
    },

    getVoltage: function (input, callback) {
        if (typeof(input) === 'function') {
            callback = input;
            input    = 0;
        }
        this.readWord(input == 1 ? 5 : input == 2 ? 6 : 1, callback);
    },

    /* returns an array of 5 integers: power source type, max, good, low, crit (mV) */
    readConfig: function (input, callback) {
        if (!('_wire' in this)) return callback("You have to call connect() first");
        
        if (typeof(input) === 'function') {
            callback = input;
            input    = 0;
        }

        var register = input == 1 ? 7 : input == 2 ? 8 : 2;
        var tries = 0;
        var request = function () {
            try {
                this._wire.readBytes(register, 5, function (err, data) {
                    if (err) {
                        if (++tries < MAXTRIES) return setTimeout(request, 333);
                        callback('Communications protocol error on read config');
                    } else {
                        var a = [];
                        for (var i = 0; i < data.length; ++i) a[i] = data[i];
                        data = a;

                        this.getFirmwareVersion(function (err, version){

                            if (err)
                                return callback(err);

                            if (version[0] == 3 && version[1] > 9 && data[0] == 255)
                                return callback('Communications protocol error on read config');

                            /* Behaviour changed at v3.10 to 5x0 so that 255 could serve as error detection */
                            if (version[0] === 3 && version[1] > 9) {
                                var n = 0;
                                data.forEach(function(i){ n += i });
                                if (n === 0) data = [255, 255, 255, 255, 255];
                            }

                            if (data[0] != 255) {
                                /* it's a cV reading that we need to convert back to mV (with 255's it's indicating a differing config) */
                                for (var i = 1; i < 5; ++i) data[i] *= 100;
                            }

                            callback(null, data);
                        });
                    }
                }.bind(this));
            } catch (e) {
                if (++tries < MAXTRIES) return setTimeout(request, 333);
                callback('I2C bus input/output error on read config');
            }
        }.bind(this);
        request();
    },

    /* takes an array of 5 integers: power source type, max, good, low, crit (mV) */
    writeConfig: function (battery, input, callback) {
        if (typeof(input) === 'function') {
            callback = input;
            input    = 0;
        }

        if (battery.length !== 5)             return callback('Invalid parameter, wrong number of arguments');
        if (battery[0] < 1 || battery[0] > 3) return callback('Invalid parameter, type outside range');

        var data = [battery[0]];
        for (var i = 1; i < 5; ++i) {
            battery[i] = parseInt(battery[i] / 100);
            data.push(battery[i]);
            battery[i] *= 100; /* for the read back we need to compare to the rounded value */
            if (data[i] < 0 || data[i] > 255) return callback('Invalid parameter, voltage outside range');
        }

        this.readConfig(input, function (err, existing){
            if (err) return callback(err);
            var same = true;
            for (var i = 0; i < 5; ++i) {
               if (existing[i] != battery[i]) same = false;
            }
            if (same) return callback();

            /* try writing the config */
            var register = input == 1 ? 7 : input == 2 ? 8 : 2;
            var tries = 0;
            var request = function () {
                try {
                    this._wire.writeBytes(register, data, function (err){
                        if (err) {
                            if (++tries < MAXTRIES) return setTimeout(request, 333);
                            callback(err);
                        } else {
                            if (++tries >= MAXTRIES) return callback('Communications protocol error on send config');

                            setTimeout(function(){ /* slight delay to allow write to take effect */
                                this.readConfig(input, function (err, existing){
                                    if (err) return setTimeout(request, 333);

                                    var worked = true;
                                    for (var i = 0; i < 5; ++i) {
                                        if (existing[i] != battery[i]) worked = false;
                                    }
                                    if (worked) return callback(); else return setTimeout(request, 333);
                                });
                            }.bind(this), 20);
                        }
                    
                    }.bind(this));
                } catch (e) {
                    if (++tries < MAXTRIES) return setTimeout(request, 333);
                    callback('I2C bus input/output error on send config');    
                }
            }.bind(this);
            request(); 

        }.bind(this));
    },

    setPowerOnDelay:  function (poweron,  callback) { this.writeWord(3, poweron, callback) },

    setShutdownDelay: function (shutdown, callback) { this.writeWord(4, shutdown, callback) },

    getPowerOnDelay:  function (callback) { this.readWord(3, callback) },

    getShutdownDelay: function (callback) { this.readWord(4, callback) },

    getFirmwareVersion: function (callback) {
        if ('_version' in this) {
            if (callback) callback(null, this._version);
        } else {
            this.readWord(9, function (err, word) {
                if (err) return callback(err);
                this._version = [ word >> 8, word & 0xFF ];
                this.getFirmwareVersion(callback);
            }.bind(this));
        }
    },

    getSerialNumber: function (callback) { this.readWord(10, callback) },

    baseReadWord: function (register, callback) {
        if (!('_wire' in this)) return callback("You have to call connect() first");

        var tries = 0;
        var request = function () {
            try {
                this._wire.readBytes(register, 2, function (err, word) {
                    if (!err) word = word[1] * 256 + word[0];
                    if ( (err || (word[0] === 0xFF && word[1] === 0xFF)) && ++tries < MAXTRIES) return setTimeout(request, 333);
                    if (!err && (word[0] === 0xFF && word[1] === 0xFF)) err = 'Communications protocol error on read word';
                    callback(err, word);
                });
            } catch (e) {
                callback('I2C bus input/output error on read word');
            }
        }.bind(this);
        request();
    },

    readWord: function (register, callback) { return this.baseReadWord(register, callback) },

    advancedReadWord: function (register, callback) {
        this.baseReadWord(register, function (err, data){
            /* try and re-read the config in the case of a high bit to counter possible i2c clock drift
               see https://github.com/raspberrypi/linux/issues/254 use if you're having consistent problems reading words */

            if (data & 32768 === 32768 || data & 128 === 128) {
                this.baseReadWord(register, function (err, data2){
                    if (data === data2) return callback(err, data);
                    this.baseReadWord(register, function (err, data3) {
                        if (data2 === data3) return callback(err, data2);
                        callback('Communications protocol error on read word, bit 15 or 7');
                    });
                }.bind(this));
            } else {
                callback(err, data);
            }
        }.bind(this));
    },

    writeWord: function (register, data, callback) {
        if (data < 0 || data > 0xFFFF) return callback('Invalid parameter, value outside range');

        /* check if word is already set */
        this.readWord(register, function (err, word){
            if (err || word === data) return callback(err);

            /* try writing */
            var tries = 0;
            var request = function () {
                try {
                    this._wire.writeBytes(register, [ data & 0xFF, data >> 8 ], function (err){
                        if (err) {
                            if (++tries < MAXTRIES) return setTimeout(request, 333);
                            callback(err);
                        } else {
                            if (++tries >= MAXTRIES) return callback('Communications protocol error on write word');

                            setTimeout(function(){ /* slight delay to allow write to take effect */
                                this.readWord(register, function (err, word){
                                    if (err || word !== data) return setTimeout(request, 333);
                                    callback();
                                });
                            }.bind(this), 20);
                        }
                    }.bind(this));
                } catch (e) {
                    if (++tries < MAXTRIES) return setTimeout(request, 333);
                    callback('I2C bus input/output error on write word');
                }
            }.bind(this);
            request();

        }.bind(this));
    }
};

function status (status) {
    this._byte = status;
}

status.prototype = {
    getByte: function () { return this._byte },
    
    getBit: function (bitnum) { return (this._byte & (1 << bitnum)) >> bitnum },

    SourceOneActive:    function () { return this.getBit(0) },
    SourceTwoActive:    function () { return this.getBit(1) },
    LEDBlue:            function () { return this.getBit(2) },
    LEDGreen:           function () { return this.getBit(3) },
    LEDRed:             function () { return this.getBit(4) },
    LEDFlashing:        function () { return this.getBit(5) },

    /* Output: 1 for NiMH, 0 for Alkaline */
    JumperState:            function () { return !this.getBit(6) },
    ForcedShutdown:         function () { return this.getBit(7) },
    PowerOnDelaySet:        function () { return this.getBit(8) },
    PowerOnDelayActive:     function () { return this.getBit(9) },
    ShutdownDelaySet:       function () { return this.getBit(10) },
    ShutdownDelayActive:    function () { return this.getBit(11) },
    CheckSourceOne:         function () { return this.getBit(12) },
    CheckSourceTwo:         function () { return this.getBit(13) },
    UserConfiguration:      function () { return this.getBit(14) },

    StatusDetail: function (callback) {
        var out = '';
        if (this.SourceOneActive())     out += "Source #1 active\n";
        if (this.SourceTwoActive())     out += "Source #2 active\n";
        if (this.LEDBlue())             out += "Source full (blue led)\n";
        if (this.LEDGreen())            out += "Source good (green led)\n";
        if (this.LEDRed())              out += "Source low (red led)\n";
        if (this.LEDFlashing())         out += "Source critical (flashing red led)\n";
        if (!this.UserConfiguration())  out += this.JumperState() ? "NiMH battery profile\n" : "Alkaline battery profile\n";
        if (this.ForcedShutdown())      out += "Forced shutdown\n";
        if (this.PowerOnDelaySet())     out += "Power on delay set\n";
        if (this.PowerOnDelayActive())  out += "Power on delay in progress\n";
        if (this.ShutdownDelaySet())    out += "Shutdown delay set\n";
        if (this.ShutdownDelayActive()) out += "Shutdown delay in progress\n";
        if (this.CheckSourceOne())      out += "Source #1 good\n"; else out += "Source #1 low/not present\n";
        if (this.CheckSourceTwo())      out += "Source #2 good\n"; else out += "Source #2 low/not present\n";
        if (this.UserConfiguration())   out += "User configured\n";
        if (out === '') return callback('Invalid status'); /* Source #1 or #2 should always be active... */
        callback(null, out);
    }
};

module.exports.mopiapi = mopiapi;
module.exports.status  = status;
module.exports.guessI2C = guessI2C;
module.exports.getApiVersion = function () { return APIVERSION };
