# Makefile for SimBaMon
# This code is copyright Hamish Cunningham and the University of Sheffield
# and is licenced under GPL 3 or any later version.

# vars #######################################################################
INSTALLED_FILES=\
  $(DESTDIR)/usr/sbin/simbamon     $(DESTDIR)/etc/init.d/simbamond \
  $(DESTDIR)/etc/default/simbamond $(DESTDIR)/usr/share/man/man8/simbamond.8.gz
INIT_LINKS=\
  $(DESTDIR)/etc/rc?.d/*simbamond
PACKAGE_FILES=\
  simbamond_1.0_all.deb simbamond_1.0_amd64.changes \
  simbamond_1.0.dsc simbamond_1.0.tar.gz simbamond-doc_1.0_all.deb

# functions ##################################################################
do-listing=\
  ls -lh $(INSTALLED_FILES) `[ -z "$(DESTDIR)" ] && echo $(INIT_LINKS)` || :

# help #######################################################################
help:
	@echo 'Makefile for SimBaMon                                         '
	@echo '                                                              '
	@echo 'Usage:                                                        '
	@echo '   make install                   installs the SimBaMon daemon'
	@echo '   make uninstall                 removes the daemon          '
	@echo '   make list                      list installed files        '
	@echo '   make package                   create .deb packaging       '
	@echo '   make package-clean             delete packaging files      '
	@echo '                                                              '

# install ####################################################################
# (if DESTDIR is set we assume this is a packaging run, not an install, and so
# don't run update-rc.d)
install:
	install -d -m 755                $(DESTDIR)/usr/sbin              && \
          install -d -m 755              $(DESTDIR)/etc/init.d            && \
          install -d -m 755              $(DESTDIR)/etc/default           && \
          install -d -m 755              $(DESTDIR)/usr/share/man/man8    && \
          install simbamond.default      $(DESTDIR)/etc/default/simbamond && \
          install -m 755 simbamon        $(DESTDIR)/usr/sbin              && \
          install -m 755 simbamond.init  $(DESTDIR)/etc/init.d/simbamond  && \
          install simbamond.8.gz         $(DESTDIR)/usr/share/man/man8
	[ -z "$(DESTDIR)" ] && update-rc.d simbamond defaults || :
	@echo 'SimBaMod installed: '
	@$(do-listing)

# uninstall ##################################################################
uninstall:
	@echo -n 'removing SimBaMod files: '
	@$(do-listing)
	[ -z "$(DESTDIR)" ] && update-rc.d -f simbamond remove || :
	sudo rm -f $(INSTALLED_FILES)
	@echo done

# manpage ####################################################################
simbamond.8: simbamond-manual.txt
	utils/txt2man -v "System Manager's Manual" -s 8 \
          -t 'simbamon' simbamond-manual.txt >simbamond.8
simbamond.8.gz: simbamond.8
	cat simbamond.8 |gzip >simbamond.8.gz

# package ####################################################################
package:
	@echo 'packaging SimBaMod...'
	@#dpkg-buildpackage -us -uc
	debuild -us -uc
	@echo ""
	cd .. && mv $(PACKAGE_FILES) simbamon/package
	@echo ""
	@ls -lh package

# package-clean ##############################################################
package-clean:
	rm -f package/*
	dh_clean

# list #######################################################################
list:
	@$(do-listing)

# phonies ####################################################################
.PHONY: install uninstall package package-clean
