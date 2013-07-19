SimBaMon: a Simple Battery Monitor daemon

This tree contains the code for a simple battery monitor daemon for projects
like Mobile Pi (MoPi) -- http://pi.gate.ac.uk/mopi.html

The daemon is implemented in three chunks:

- /etc/simbamon.conf    -- a set of config variables
- /usr/sbin/simbamon    -- the daemon itself
- /etc/init.d/simbamond -- init interface to start/stop/etc. the daemon

There are also:

- links to the init interface from /etc/rc?.d which is managed by update-rc.d
- a link to /etc/simbamon.conf from /etc/default/simbamon
- (when running) a process ID file in /var/run/simbamon.pid

The intial target operating system is the Raspian distribution of Debian, for
the Raspberry Pi. It is intended to be compatible with other *nixes.

This code is copyright Hamish Cunningham and the University of Sheffield and
is licenced under GPL 3 or any later version.
