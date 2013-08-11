BlinkIP: an IP notification daemon for the Raspberry Pi.

This tree contains the code for a simple IP notification daemon derived from
Chris Meyers' perl script described here --
http://chrismeyers.org/2012/06/02/raspberry-pi-no-hdmi-cable-or-no-hdmi-display-blink-ip-address-to-ok-led/
-- and here -- https://gist.github.com/chrismeyersfsu/2858824
(thanks Chris!).

See also http://pi.gate.ac.uk/pages/blinkip.html

The daemon is implemented in three chunks:

- /etc/blinkip.conf    -- a set of config variables
- /usr/sbin/blinkip    -- the daemon itself
- /etc/init.d/blinkipd -- init interface to start/stop/etc. the daemon

There are also:

- links to the init interface from /etc/rc?.d which is managed by update-rc.d
- a link to /etc/blinkip.conf from /etc/default/blinkip
- (when running) a process ID file in /var/run/blinkip.pid
- a source file for the man page (manpage.txt) and the man page itself
  (blinkip.8)

To test and debug, first set DEBUG=on in blinkip.conf and reinstall/restart
the service; then the utils directory contains a monitor-log.sh script which
greps the most recent blinkip entries from syslog.

(The utils directory also contains a great script called txt2man from
http://mvertes.free.fr/ that we use to maintain the manpage.)

The target operating system is the Raspian distribution of Debian, for the
Raspberry Pi.

This code is copyright Hamish Cunningham and the University of Sheffield and
is licenced under GPL 3 or any later version. Project started August 2013.
