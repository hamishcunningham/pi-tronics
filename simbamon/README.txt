SimBaMon: a Simple Battery Monitor daemon

-----------------------------------------------------------------------------
This tree contains the code for a simple battery monitor daemon for projects
like Mobile Pi (MoPi) -- http://pi.gate.ac.uk/pages/mopi.html

The target operating system is the Raspian distribution of Debian, for the
Raspberry Pi. (It also works in simulation mode on Ubuntu and is intended to
be compatible with other *nixes.)

The code is copyright Hamish Cunningham and the University of Sheffield and is
licenced under GPL 3 or any later version.

The daemon is implemented in three chunks:

- /etc/default/simbamond -- a set of config variables (see
  ./simbamond.default)
- /usr/sbin/simbamon     -- the daemon itself (./simbamon)
- /etc/init.d/simbamond  -- an init interface used by the operating system to
  start/stop/etc. the daemon (./simbamond.init)

There are also:

- links to the init interface from /etc/rc?.d which are managed by update-rc.d
- (when running) a process ID file in /var/run/simbamon.pid
- a source file for the man page (man/simbamond.txt) and the man pages
  themselves (man/simbamon[d].8 and their compressed versions)

-----------------------------------------------------------------------------
To install:

- on Raspbian:
  - sudo apt-get install simbamond
  - alternatively, if you want the latest development snapshot:
    - add this line to /etc/apt/sources.list
      - deb http://ppa.launchpad.net/hamish-dcs/pi-gate-snapshots/ubuntu
        precise main
    - import the encryption key from Ubuntu so that the Pi can verify the
      package's validity:
      - gpg --keyserver keyserver.ubuntu.com --recv-key 6C12C1CF
      - gpg -a --export 6C12C1CF |sudo apt-key add -
    - update your list of available packages (this may take a couple of
      minutes):
      - sudo apt-get update
    - install the package:
      - sudo apt-get install simbamond
- on Ubuntu (for testing and debugging):
  - sudo add-apt-repository ppa:hamish-dcs/pi-gate
    - (use ppa:hamish-dcs/pi-gate-snapshots for development builds)
  - sudo apt-get update
  - sudo apt-get install simbamond
  - this will generate a failure message as Ubuntu lacks the gpio command --
    use simulation mode as described below

-----------------------------------------------------------------------------
To test and debug:

First restart the service with the -d (debug) and/or -s (simulation) flags;
then the utils directory contains these scripts:

- monitor-log.sh: greps the most recent simbamon entries from syslog
- set-simulation-level.sh: continually reads a simulation number (3 bit
  binary) from the terminal and writes it into the /tmp file where the debug
  rig will read it -- try "111" or "000" for starters, while watching the log
  entries

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
