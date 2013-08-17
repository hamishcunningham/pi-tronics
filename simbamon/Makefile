# Makefile for SimBaMon
# This code is copyright Hamish Cunningham and the University of Sheffield
# and is licenced under GPL 3 or any later version.

# vars #######################################################################
VERSION=1.0
P=simbamond
INSTALLED_FILES=\
  $(DESTDIR)/usr/sbin/simbamon \
  $(DESTDIR)/etc/init.d/$(P) \
  $(DESTDIR)/etc/default/$(P) \
  $(DESTDIR)/usr/share/man/man8/simbamon.8.gz \
  $(DESTDIR)/usr/share/man/man8/$(P).8.gz
INIT_LINKS=\
  $(DESTDIR)/etc/rc?.d/*$(P)
PACKAGE_FILES=\
  $(P)_$(VERSION)*.deb \
  $(P)_$(VERSION)*.dsc \
  $(P)_$(VERSION)*.tar.gz \
  $(P)_$(VERSION)*.changes \
  $(P)_$(VERSION)*.build

# functions ##################################################################
do-listing=\
  ls $(INSTALLED_FILES) `[ -z "$(DESTDIR)" ] && echo $(INIT_LINKS)` || :

# help #######################################################################
help:
	@echo 'Makefile for SimBaMon                                         '
	@echo '                                                              '
	@echo 'Usage:                                                        '
	@echo '   make install                   installs the SimBaMon daemon'
	@echo '   make uninstall                 removes the daemon          '
	@echo '   make list                      list installed files        '
	@echo '   make package                   create .deb/.dcs packagings '
	@echo '   make package-upload            upload to PPA repository    '
	@echo '   make package-clean             delete tmp packaging files  '
	@echo '                                                              '

# install ####################################################################
# (if DESTDIR is set we assume this is a packaging run, not an install, and so
# don't run update-rc.d)
install:
	install -d -m 755              $(DESTDIR)/usr/sbin
	install -d -m 755              $(DESTDIR)/etc/init.d
	install -d -m 755              $(DESTDIR)/etc/default
	install -d -m 755              $(DESTDIR)/usr/share/man/man8
	install simbamond.default      $(DESTDIR)/etc/default/simbamond
	install -m 755 simbamon        $(DESTDIR)/usr/sbin
	install -m 755 simbamond.init  $(DESTDIR)/etc/init.d/simbamond
	install simbamond.8.gz         $(DESTDIR)/usr/share/man/man8
	install simbamon.8.gz          $(DESTDIR)/usr/share/man/man8
	[ -z "$(DESTDIR)" ] && update-rc.d simbamond defaults || :
	@echo 'SimBaMod installed: '
	@$(do-listing)

# uninstall ##################################################################
uninstall:
	@echo 'removing SimBaMod files: '
	@$(do-listing)
	[ -z "$(DESTDIR)" ] && update-rc.d -f $(P) remove || :
	sudo rm -f $(INSTALLED_FILES)
	@echo done

# manpage ####################################################################
simbamond.8: simbamond-manual.txt
	utils/txt2man -v "System Manager's Manual" -s 8 \
          -t 'simbamon' simbamond-manual.txt >simbamond.8
	sed -i 1d simbamond.8  # fix error from lintian about ." macro
	cat simbamond.8 |gzip >simbamond.8.gz
	cp simbamond.8.gz simbamon.8.gz

# package ####################################################################
package: package-unstable package-precise
	@echo "\nunstable:"
	@ls -lh package/unstable
	@echo "\nprecise:"
	@ls -lh package/precise
package-unstable:
	@echo 'packaging SimBaMod for Debian unstable...'
	rm -f package/unstable/*
	sed -i \
          's!\(^$(P) ('$(VERSION)') \)[a-z]*!\1unstable!' debian/changelog
	debuild
	@echo ""
	cd .. && for f in $(PACKAGE_FILES); do \
          [ -f $$f ] && mv $$f simbamon/package/unstable; done
package-precise:
	@echo 'packaging SimBaMod for Ubuntu precise...'
	rm -f package/precise/*
	sed -i \
          's!\(^$(P) ('$(VERSION)') \)[a-z]*!\1precise!' debian/changelog
	debuild -S
	sed -i \
          's!\(^$(P) ('$(VERSION)') \)[a-z]*!\1unstable!' debian/changelog
	@echo ""
	cd .. && for f in $(PACKAGE_FILES); do \
          [ -f $$f ] && mv $$f simbamon/package/precise; done
package-info:
	apt-cache showpkg simbamond

# package-upload #############################################################
package-upload:
	cd package/precise && dput ppa:hamish-dcs/pi-gate \
          $(P)_$(VERSION)_source.changes
	cd package/precise && mv $(P)_$(VERSION)*.ppa.upload /tmp || :

# package-clean ##############################################################
package-clean:
	dh_clean

# list #######################################################################
list:
	@$(do-listing)

# phonies ####################################################################
.PHONY: install uninstall package package-unstable package-precise
.PHONY: package-upload package-clean list
