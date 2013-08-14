SimBaMon: a Simple Battery Monitor daemon

This tree contains the code for a simple battery monitor daemon for projects
like Mobile Pi (MoPi) -- http://pi.gate.ac.uk/pages/mopi.html

The daemon is implemented in three chunks:

- /etc/default/simbamon -- a set of config variables
- /usr/sbin/simbamon    -- the daemon itself
- /etc/init.d/simbamond -- init interface to start/stop/etc. the daemon

There are also:

- links to the init interface from /etc/rc?.d which is managed by update-rc.d
- (when running) a process ID file in /var/run/simbamon.pid
- a source file for the man page (simbamond-manual.txt) and the man page
  itself (simbamon.8)

To test and debug, first restart the service with the -d (debug) and/or -s
(simulation) flags; then the utils directory contains these scripts:

- monitor-log.sh: greps the most recent simbamon entries from syslog
- set-simulation-level.sh: continually reads a simulation number (3 bit
  binary) from the terminal and writes it into the /tmp file where the debug
  rig will read it

(The utils directory also contains a great script called txt2man from
http://mvertes.free.fr/ that we use to maintain the manpage.)

The intial target operating system is the Raspian distribution of Debian, for
the Raspberry Pi. It is intended to be compatible with other *nixes.

This code is copyright Hamish Cunningham and the University of Sheffield and
is licenced under GPL 3 or any later version. Project started July 2013.
