# Makefile for marvin
# This code is copyright Hamish Cunningham and the University of Sheffield
# and is licenced under GPL 3 or any later version.

# vars #######################################################################
VERSION=0.1
NEXT_SNAP=2
P=marvind
D=marvin
MARVIN=marvin
MARVINCLI=marvincli
MARVINAPI=marvinapi.py
PD=package/$(VERSION)
INSTALLED_FILES=\
  $(DESTDIR)/usr/sbin/$(D) \
  $(DESTDIR)/usr/sbin/$(MARVIN) \
  $(DESTDIR)/usr/sbin/$(MARVINCLI) \
  $(DESTDIR)/usr/sbin/$(MARVINAPI) \
  $(DESTDIR)/etc/init.d/$(P) \
  $(DESTDIR)/etc/default/$(P) \
  $(DESTDIR)/usr/share/man/man8/$(D).8.gz \
  $(DESTDIR)/usr/share/man/man8/$(P).8.gz \
  $(DESTDIR)/usr/share/man/man8/$(MARVIN).8.gz \
  $(DESTDIR)/usr/share/man/man8/$(MARVINCLI).8.gz \
  $(DESTDIR)/usr/share/man/man8/$(MARVINAPI).8.gz
INIT_LINKS=\
  $(DESTDIR)/etc/rc?.d/*$(P)
PACKAGE_FILES=\
  $(P)_$(VERSION)*.deb \
  $(P)_$(VERSION)*.dsc \
  $(P)_$(VERSION)*.tar.xz \
  $(P)_$(VERSION)*.changes \
  $(P)_$(VERSION)*.build
NOW:=$(shell date "+%Y-%m-%d-%R" |sed 's,:,,')
MAJOR_VERSION:=$(shell echo $(VERSION) |sed 's,\([0-9]*\)\..*,\1,')
MINOR_VERSION:=$(shell echo $(VERSION) |sed 's,.*\.,,')
SNAPSHOT_VERSION:=$(VERSION)+$(NEXT_SNAP)
SNAPSHOT:=$(SNAPSHOT_VERSION)-SNAPSHOT-$(NOW)
SNAPD:=$(PD)/snapshots/$(SNAPSHOT)

# functions ##################################################################
do-listing=\
  ls $(INSTALLED_FILES) `[ -z "$(DESTDIR)" ] && echo $(INIT_LINKS)` || :

# help #######################################################################
help:
	@echo 'Makefile for marvin                                         '
	@echo '                                                              '
	@echo 'Usage:                                                        '
	@echo '   make install                   installs the marvin daemon'
	@echo '   make uninstall                 removes the daemon          '
	@echo '   make list                      list installed files        '
	@echo '   make package                   create .deb/.dcs packagings '
	@echo '   make package-upload            upload to PPA repository    '
	@echo '   make package-clean             delete tmp packaging files  '
	@echo '   make package-info              apt-cache showpkg           '
	@echo '   make package-purge             apt-get purge               '
	@echo '   make package-version           update the changelog        '
	@echo '   make print-versions            print current version #s    '
	@echo '                                                              '

# show versions ##############################################################
print-versions:
	@echo "VERSION: $(VERSION); SNAPSHOT_VERSION: $(SNAPSHOT_VERSION)"

# install ####################################################################
# (if DESTDIR is set we assume this is a packaging run, not an install, and so
# don't run update-rc.d)
install:
	install -d -m 755           $(DESTDIR)/usr/sbin
	install -d -m 755           $(DESTDIR)/etc/init.d
	install -d -m 755           $(DESTDIR)/etc/default
	install -d -m 755           $(DESTDIR)/usr/share/man/man8
	install $(P).default        $(DESTDIR)/etc/default/$(P)
	install -m 755 $(D)         $(DESTDIR)/usr/sbin
	install -m 755 $(P).init    $(DESTDIR)/etc/init.d/$(P)
	install -m 755 $(MARVIN)      $(DESTDIR)/usr/sbin
	install -m 755 $(MARVINCLI)   $(DESTDIR)/usr/sbin
	install -m 644 $(MARVINAPI)   $(DESTDIR)/usr/sbin
	install man/$(P).8.gz       $(DESTDIR)/usr/share/man/man8
	install man/$(D).8.gz       $(DESTDIR)/usr/share/man/man8
	install man/$(MARVIN).8.gz    $(DESTDIR)/usr/share/man/man8
	install man/$(MARVINCLI).8.gz $(DESTDIR)/usr/share/man/man8
	install man/$(MARVINAPI).8.gz $(DESTDIR)/usr/share/man/man8
	[ -z "$(DESTDIR)" ] && update-rc.d $(P) defaults || :
	@echo 'marvin installed: '
	@$(do-listing)

# uninstall ##################################################################
uninstall:
	@echo 'removing marvin files: '
	@$(do-listing)
	[ -z "$(DESTDIR)" ] && update-rc.d -f $(P) remove || :
	sudo rm -f $(INSTALLED_FILES)
	@echo done

# manpage ####################################################################
man: man/$(P).txt man/$(MARVIN).txt
	cd man; ../utils/txt2man -v "System Manager's Manual" -s 8 \
          -t '$(D)' $(P).txt >$(P).8; \
	sed -i 1d $(P).8;  # fix error from lintian about ." macro \
	cat $(P).8 |gzip >$(P).8.gz; cp $(P).8.gz $(D).8.gz
	cd man; ../utils/txt2man -v "System Manager's Manual" -s 8 \
          -t '$(MARVIN)' $(MARVIN).txt >$(MARVIN).8; \
	sed -i 1d $(MARVIN).8;  # fix error from lintian about ." macro \
	cat $(MARVIN).8 |gzip >$(MARVIN).8.gz;

# package ####################################################################
version:
	@for f in marvind.default marvincli marvinapi.py; do \
          sed -i 's,^VERSION=.*,VERSION=\"'$(VERSION)'\",' $$f; done
package: version man package-unstable package-precise
	@echo "\nunstable:"
	@ls -lh $(PD)/unstable
	@echo "\nprecise:"
	@ls -lh $(PD)/precise
package-unstable:
	@echo 'packaging marvin for Debian unstable...'
	mkdir -p $(PD)/unstable
	rm -f $(PD)/unstable/*
	sed -i \
          's,\(^$(P) ('$(VERSION)') \)[a-z]*,\1unstable,' debian/changelog
	debuild -Ipackage
	@echo ""
	cd .. && for f in $(PACKAGE_FILES); do \
          [ -f $$f ] && mv $$f $(D)/$(PD)/unstable || :; done
package-precise:
	@echo 'packaging marvin for Ubuntu precise...'
	mkdir -p $(PD)/precise
	rm -f $(PD)/precise/*
	sed -i 's,\(^$(P) ('$(VERSION)') \)[a-z]*,\1precise,' debian/changelog
	debuild -S -Ipackage
	sed -i 's,\(^$(P) ('$(VERSION)') \)[a-z]*,\1unstable,' \
          debian/changelog
	@echo ""
	cd .. && for f in $(PACKAGE_FILES); do \
          [ -f $$f ] && mv $$f $(D)/$(PD)/precise || :; done
snapshot-version:
	@for f in marvind.default marvincli marvinapi.py; do \
          sed -i 's,^VERSION=.*,VERSION=\"'$(SNAPSHOT_VERSION)'\",' $$f; done
	sed -i 's,^NEXT_SNAP=.*,NEXT_SNAP='$$(($(NEXT_SNAP) + 1))',' Makefile
snapshot: snapshot-version
	@echo "packaging marvin SNAPSHOT $(SNAPSHOT)..."
	mkdir -p $(SNAPD)
	rm -rf $(SNAPD)/*
	sed -i -e 's,\(^$(P) ('$(VERSION)') \)[a-z]*,\1precise,' \
	       -e 's,^$(P) ($(VERSION),$(P) ($(SNAPSHOT_VERSION),' \
          debian/changelog
	@head -1 debian/changelog
	debuild -S -Ipackage
	sed -i -e 's,^$(P) ($(SNAPSHOT_VERSION),$(P) ($(VERSION),' \
               -e 's,\(^$(P) ('$(VERSION)') \)[a-z]*,\1unstable,' \
          debian/changelog
	@head -1 debian/changelog
	@echo ""
	cd .. && for f in $(PACKAGE_FILES); do \
          [ -f $$f ] && mv $$f $(D)/$(SNAPD) || :; done
	@echo "\nsnapshot:"
	@ls -lhR $(SNAPD)

# package-upload #############################################################
package-upload:
	cd $(PD)/precise && dput ppa:hamish-dcs/pi-gate \
          $(P)_$(VERSION)_source.changes
	cd $(PD)/precise && mv $(P)_$(VERSION)*.ppa.upload /tmp || :

# snapshot-upload ############################################################
# relies on lexical ordering of snapshot names to pick the latest one
# (apt also relies on this ordering)
snapshot-upload:
	cd package/$(VERSION)/snapshots; \
	LAST_SNAP=`ls -r |head -1`; \
        cd $$LAST_SNAP && \
          dput ppa:hamish-dcs/pi-gate-snapshots $(P)*_source.changes; \
	mv $(P)_*.ppa.upload /tmp || :

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

# test #######################################################################
#test:
#	echo; sudo python ./api-test.py |pr -l 33 -t -2 -w 132; echo

# list #######################################################################
list:
	@$(do-listing)

# phonies ####################################################################
.PHONY: install uninstall package package-unstable package-precise
.PHONY: package-upload package-clean list version snapshot-version
