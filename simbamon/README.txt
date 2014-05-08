SimBaMon: a Simple Battery Monitor daemon

-----------------------------------------------------------------------------
This tree contains the code for a simple battery monitor daemon for projects
like Mobile Pi (MoPi) -- http://pi.gate.ac.uk/mopi

The target operating system is the Raspian distribution of Debian, for the
Raspberry Pi. (It can also work in debug mode on Ubuntu and is intended to be
compatible with other *nixes.)

The code is copyright Hamish Cunningham and the University of Sheffield and is
licenced under GPL 3 or any later version.

-----------------------------------------------------------------------------
The daemon is implemented in three chunks:

- /etc/default/simbamond -- a set of config variables and support code (see
  ./simbamond.default)
- /usr/sbin/simbamon     -- the daemon itself (./simbamon)
- /etc/init.d/simbamond  -- an init interface used by the operating system to
  start/stop/etc. the daemon (./simbamond.init)

There are also:

- a configuration script in /usr/sbin/mopi (with manpage) (see ./mopi)
- a command-line interface to the board (./mopicli), used by mopi
- a Python API for the board (./mopiapi.py), used by mopicli
- links to the init interface from /etc/rc?.d which are managed by update-rc.d
- (when running) a process ID file in /var/run/simbamon.pid
- (when running) a "first run after boot" indicator file in /tmp
- source files for the man pages (man/\*.txt) and the man pages themselves
  (man/\*.8 and their compressed versions)

-----------------------------------------------------------------------------
To install (see also http://pi.gate.ac.uk/pages/download.html):

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
  - this will generate a failure messages relating to I2C -- use the -d option
    to suppress

-----------------------------------------------------------------------------
To test and debug:

First restart the service with the -d (debug) flag; then the utils directory
contains monitor-log.sh which greps the most recent simbamon entries from
syslog. If you want to do simulation, trawl previous commits for
set-simulation-level.sh which continually reads a simulation status from the
terminal and writes it into the /tmp file where the debug rig will read it.

(The utils directory also contains a great script called txt2man from
http://mvertes.free.fr/ that we use to maintain the manpage, and an example
script to read battery level.)

-----------------------------------------------------------------------------
To configure:

sudo mopi

-----------------------------------------------------------------------------
To release:

- before a release
  - use snapshots to verify that the build is a good one, that it installs
    correctly from the PPA and so on
    - set NEXT_SNAP to 1 in Makefile for first in series, then increment
  - update the version in the Makefile and do "make package-version" to add a
    changelog entry for the release (remember to ensure the maintainer line
    matches the others exactly!)
    - for individual snapshots *don't* do a changelog entry
- to release on the PPAs, "make package" and "make package-upload" (think
  carefully before the latter -- it can't be reverted!)
- after a release, do "make package-version" and add a changelog entry to note
  the move to the next series of snapshots
- to do a snapshot PPA release, "make snapshot" and "make snapshot-upload"

Note: if you hit the 10th snapshot the ordering doesn't work any more -- as a
workaround, increment the minor version number and start over at snapshot 0.

Versions which are uploaded to the PPAs should be checked in (from the
"package" directory).

Note that the changelog is written for "Debian unstable" and then modified
(and later reverted) in place by the Makefile targets when building for other
targets. Similarly the changelog version is modified (and reverted) by the
snapshot build.
-----------------------------------------------------------------------------
