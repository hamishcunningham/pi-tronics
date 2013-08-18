# Makefile for SimBaMon
# This code is copyright Hamish Cunningham and the University of Sheffield
# and is licenced under GPL 3 or any later version.

# vars #######################################################################
MINORVERSION=1
VERSION=1.$(MINORVERSION)
SNAPSHOT=$(VERSION)+`expr $(MINORVERSION) + 1`-SNAPSHOT-`date "+%Y-%m-%d"`
P=simbamond
PD=package/$(VERSION)
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
	@echo '   make package-info              apt-cache showpkg           '
	@echo '   make package-purge             apt-get purge               '
	@echo '   make package-version           update the changelog        '
	@echo '                                                              '

# install ####################################################################
# (if DESTDIR is set we assume this is a packaging run, not an install, and so
# don't run update-rc.d)
install:
	install -d -m 755         $(DESTDIR)/usr/sbin
	install -d -m 755         $(DESTDIR)/etc/init.d
	install -d -m 755         $(DESTDIR)/etc/default
	install -d -m 755         $(DESTDIR)/usr/share/man/man8
	install $(P).default      $(DESTDIR)/etc/default/$(P)
	install -m 755 simbamon   $(DESTDIR)/usr/sbin
	install -m 755 $(P).init  $(DESTDIR)/etc/init.d/$(P)
	install $(P).8.gz         $(DESTDIR)/usr/share/man/man8
	install simbamon.8.gz     $(DESTDIR)/usr/share/man/man8
	[ -z "$(DESTDIR)" ] && update-rc.d $(P) defaults || :
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
$(P).8: $(P)-manual.txt
	utils/txt2man -v "System Manager's Manual" -s 8 \
          -t 'simbamon' $(P)-manual.txt >$(P).8
	sed -i 1d $(P).8  # fix error from lintian about ." macro
	cat $(P).8 |gzip >$(P).8.gz
	cp $(P).8.gz simbamon.8.gz

# package ####################################################################
package: package-unstable package-precise
	@echo "\nunstable:"
	@ls -lh $(PD)/unstable
	@echo "\nprecise:"
	@ls -lh $(PD)/precise
package-unstable:
	@echo 'packaging SimBaMod for Debian unstable...'
	mkdir -p $(PD)/unstable
	rm -f $(PD)/unstable/*
	sed -i \
          's!\(^$(P) ('$(VERSION)') \)[a-z]*!\1unstable!' debian/changelog
	debuild -Ipackage
	@echo ""
	cd .. && for f in $(PACKAGE_FILES); do \
          [ -f $$f ] && mv $$f simbamon/$(PD)/unstable; done
package-precise:
	@echo 'packaging SimBaMod for Ubuntu precise...'
	mkdir -p $(PD)/precise
	rm -f $(PD)/precise/*
	sed -i \
          's!\(^$(P) ('$(VERSION)') \)[a-z]*!\1precise!' debian/changelog
	debuild -S -Ipackage
	sed -i \
          's!\(^$(P) ('$(VERSION)') \)[a-z]*!\1unstable!' debian/changelog
	@echo ""
	cd .. && for f in $(PACKAGE_FILES); do \
          [ -f $$f ] && mv $$f simbamon/$(PD)/precise; done

# package-upload #############################################################
package-upload:
	cd $(PD)/precise && dput ppa:hamish-dcs/pi-gate \
          $(P)_$(VERSION)_source.changes
	cd $(PD)/precise && mv $(P)_$(VERSION)*.ppa.upload /tmp || :

# package utilities
package-info:
	apt-cache showpkg $(P)
package-purge:
	apt-get purge $(P)
package-clean:
	dh_clean
package-version:
	dch -i
	@echo 'remember to change VERSION in the Makefile!'

# list #######################################################################
list:
	@$(do-listing)

# phonies ####################################################################
.PHONY: install uninstall package package-unstable package-precise
.PHONY: package-upload package-clean list
