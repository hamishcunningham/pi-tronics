SimBaMon: a Simple Battery Monitor daemon

This tree contains the code for a simple battery monitor daemon for projects
like Mobile Pi (MoPi) -- http://pi.gate.ac.uk/pages/mopi.html

The daemon is implemented in three chunks:

- /etc/simbamon.conf    -- a set of config variables
- /usr/sbin/simbamon    -- the daemon itself
- /etc/init.d/simbamond -- init interface to start/stop/etc. the daemon

There are also:

- links to the init interface from /etc/rc?.d which is managed by update-rc.d
- a link to /etc/simbamon.conf from /etc/default/simbamon
- (when running) a process ID file in /var/run/simbamon.pid

To test and debug, first set DEBUG=on in simbamon.conf and reinstall/restart
the service; then the utils directory contains these scripts:

- monitor-log.sh: greps the most recent simbamon entries from syslog
- set-simulation-level.sh: continually reads a simulation number (3 bit
  binary) from the terminal and writes it into the /tmp file where the debug
  rig will read it

The intial target operating system is the Raspian distribution of Debian, for
the Raspberry Pi. It is intended to be compatible with other *nixes.

This code is copyright Hamish Cunningham and the University of Sheffield and
is licenced under GPL 3 or any later version. Project started July 2013.
