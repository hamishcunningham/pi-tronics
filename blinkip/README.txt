BlinkIP: an IP notification daemon for the Raspberry Pi.

-----------------------------------------------------------------------------
This tree contains the code for a simple IP notification daemon. See
http://pi.gate.ac.uk/pages/blinkip.html for details.

The target operating system is the Raspian distribution of Debian GNU Linux,
for the Raspberry Pi. Other Debian derivatives (e.g. Ubuntu) will work to a
degree, but we rely on the presence of /sys/class/leds/led0 to switch the Pi's
status light on and off.

The daemon will pause around 30 seconds after startup, then blink the IP
address 10 times, pausing 30 secs between each, then exit. The timings and
number of iterations are configurable as detailed below.

The code is copyright Hamish Cunningham and the University of Sheffield and is
licenced under GPL 3 or any later version.

The daemon is implemented in three chunks:

- /etc/default/blinkipd -- a set of config variables (see ./blinkipd.default)
- /usr/sbin/blinkip     -- the daemon itself (./blinkip)
- /etc/init.d/blinkipd  -- an init interface used by the operating system to
  start/stop/etc. the daemon (./blinkipd.init)

There are also:

- links to the init interface from /etc/rc?.d which are managed by update-rc.d
- (when running) a process ID file in /var/run/blinkip.pid
- a source file for the man page (man/blinkipd.txt) and the man pages
  themselves (man/blinkip[d].8 and their compressed versions)

The LED blink code was inspired by Chris Meyers' perl script described here --
http://chrismeyers.org/2012/06/02/raspberry-pi-no-hdmi-cable-or-no-hdmi-display-blink-ip-address-to-ok-led/
-- and here -- https://gist.github.com/chrismeyersfsu/2858824 (thanks Chris!).

-----------------------------------------------------------------------------
To install on Raspbian:

- add this line to /etc/apt/sources.list
  - deb http://ppa.launchpad.net/hamish-dcs/pi-gate/ubuntu precise main
- import the encryption key from Ubuntu so that the Pi can verify the
  package's validity:
  - gpg --keyserver keyserver.ubuntu.com --recv-key 6C12C1CF
  - gpg -a --export 6C12C1CF |sudo apt-key add -
- update your list of available packages (this may take a couple of minutes):
  - sudo apt-get update
- install the package:
  - sudo apt-get install blinkipd

If you wish to use snapshot builds, add this line to sources.list
- deb http://ppa.launchpad.net/hamish-dcs/pi-gate-snapshots/ubuntu precise main

-----------------------------------------------------------------------------
To test and debug:

To generate more detailed logging, restart the daemon with the "-d" flag,
e.g.:

  sudo service blinkipd stop
  sudo service blinkipd start -d

The utils directory also contains these scripts:

- monitor-log.sh: greps the most recent blinkip entries from syslog
- blinkip.sh: a stand-alone script which does the blinking -- call it with an
  IP address like this: 123 456 789 000

(The utils directory also contains a great script called txt2man from
http://mvertes.free.fr/ that we use to maintain the manpage.)

-----------------------------------------------------------------------------
To release:

- before a release
  - use snapshots to verify that the build is a good one, that it installs
    correctly from the PPA and so on
  - update the version in the Makefile and do "make package-version" to add a
    changelog entry for the release (remember to ensure the maintainer line
    matches the others exactly!)
- to release on the PPAs, "make package" and "make package-upload" (think
  carefully before the latter -- it can't be reverted!)
- after a release, do "make package-version" and add a changelog entry to note
  the move to the next series of snapshots
- to do a snapshot PPA release, "make snapshot" and "make snapshot-upload"

Versions which are uploaded to the PPAs should be checked in (from the
"package" directory).

Note that the changelog is written for "Debian unstable" and then modified
(and later reverted) in place by the Makefile targets when building for other
targets. Similarly the changelog version is modified (and reverted) by the
snapshot build.
-----------------------------------------------------------------------------
