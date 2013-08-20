SimBaMon: a Simple Battery Monitor daemon

-----------------------------------------------------------------------------
This tree contains the code for a simple battery monitor daemon for projects
like Mobile Pi (MoPi) -- http://pi.gate.ac.uk/pages/mopi.html

The daemon is implemented in three chunks:

- /etc/default/simbamond -- a set of config variables; see ./simbamond.default
- /usr/sbin/simbamon     -- the daemon itself
- /etc/init.d/simbamond  -- init interface to start/stop/etc. the daemon; see
  ./simbamond.init

There are also:

- links to the init interface from /etc/rc?.d which is managed by update-rc.d
- (when running) a process ID file in /var/run/simbamon.pid
- a source file for the man page (man/simbamond.txt) and the man pages
  themselves (man/simbamon[d].8 and their compressed versions)

-----------------------------------------------------------------------------
To install:

- on Raspbian
  - TODO
- on Ubuntu (for testing and debugging:
  - sudo add-apt-repository ppa:hamish-dcs/pi-gate
  - sudo apt-get update
  - sudo apt-get install simbamond
  - this will generate a failure message as Ubuntu lacks the gpio command --
    use simulation mode as described below

-----------------------------------------------------------------------------
To test and debug, first restart the service with the -d (debug) and/or -s
(simulation) flags; then the utils directory contains these scripts:

- monitor-log.sh: greps the most recent simbamon entries from syslog
- set-simulation-level.sh: continually reads a simulation number (3 bit
  binary) from the terminal and writes it into the /tmp file where the debug
  rig will read it

(The utils directory also contains a great script called txt2man from
http://mvertes.free.fr/ that we use to maintain the manpage.)

-----------------------------------------------------------------------------
To package:

- before a release, update the version in the Makefile and do
  "make package-version" to add a changelog entry for the release
- to release, "make package" and "make package-upload"
- after a release, do "make package-version" and add a changelog entry to note
  the move to snapshots
- to do a snapshot release, "make snapshot" and "make snapshot-upload"

-----------------------------------------------------------------------------
The intial target operating system is the Raspian distribution of Debian, for
the Raspberry Pi. It is intended to be compatible with other *nixes.

This code is copyright Hamish Cunningham and the University of Sheffield and
is licenced under GPL 3 or any later version. Project started July 2013.
-----------------------------------------------------------------------------
