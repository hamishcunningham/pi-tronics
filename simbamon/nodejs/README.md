# mopiapi

NodeJS Interface to the MoPi battery power add-on board for the Raspberry Pi.
(http://pi.gate.ac.uk/mopi). This is a port of the python libary of the same
name.

I have tried to keep the API as close as possible to the python library version,
except that it uses callbacks instead of function return values.

Note: This module uses the nodejs i2c module, which does not work on some older
versions of nodejs. It definitely works on v0.10.24 and later though.

## Usage

```javascript

var mopiapi = require('mopiapi');

var mopi = new mopiapi.mopiapi();

mopi.connect(function(err){
    if (err) return console.log(err);

    mopi.getStatus(function (err, status){
        if (err) return console.log("Error", err);

        status = new mopiapi.status(status);

        status.StatusDetail(function(err, detail){
            if (err) return console.log("Error", err);
            console.log(detail);
        });
    });
});
````

It has all of the other methods that the Python version has as well. E.g to get the
voltage on source 2:

```javascript
mopi.getVoltage(2, function(err, voltage){ });
````
