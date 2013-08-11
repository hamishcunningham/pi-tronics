# Makefile for SimBaMon
# This code is copyright Hamish Cunningham and the University of Sheffield
# and is licenced under GPL 3 or any later version.

# vars #######################################################################
INSTALLED_FILES=\
$(DESTDIR)/etc/simbamon.conf    $(DESTDIR)/usr/sbin/simbamon \
$(DESTDIR)/etc/init.d/simbamond $(DESTDIR)/etc/default/simbamon \
$(DESTDIR)/etc/rc?.d/*simbamond $(DESTDIR)/usr/share/man/man8/simbamon.8.gz
SUDO=/usr/bin/sudo

# help #######################################################################
help:
	@echo 'Makefile for SimBaMon                                         '
	@echo '                                                              '
	@echo 'Usage:                                                        '
	@echo '   make install                   installs the SimBaMon daemon'
	@echo '   make uninstall                 removes the daemon          '
	@echo '   make list                      list installed files        '
	@echo '                                                              '

# install ####################################################################
install:
	SD=`which sudo` && \
          $$SD mkdir -p                    $(DESTDIR)/usr/sbin             && \
          $$SD mkdir -p                    $(DESTDIR)/etc/init.d           && \
          $$SD mkdir -p                    $(DESTDIR)/etc/default          && \
          $$SD mkdir -p                    $(DESTDIR)/usr/share/man/man8   && \
          $$SD install simbamon.conf       $(DESTDIR)/etc                  && \
          $$SD install -m 755 simbamon     $(DESTDIR)/usr/sbin             && \
          $$SD install -m 755 simbamond    $(DESTDIR)/etc/init.d           && \
          $$SD ln -fs $(DESTDIR)/etc/simbamon.conf $(DESTDIR)/etc/default/simbamon && \
          $$SD install -D simbamon.8.gz    $(DESTDIR)/usr/share/man/man8   && \
          cd $(DESTDIR)/etc/init.d && $$SD update-rc.d simbamond defaults
	@echo 'SimBaMod installed: '
	@ls -l $(INSTALLED_FILES) || :

# uninstall ##################################################################
uninstall:
	@echo -n 'removing SimBaMod files: '
	@ls $(INSTALLED_FILES) || :
	sudo rm -f $(INSTALLED_FILES)
	@echo done

# manpage ####################################################################
simbamon.8: manpage.txt
	utils/txt2man -v "System Manager's Manual" -s 8 \
          -t 'simbamon' manpage.txt >simbamon.8
simbamon.8.gz: simbamon.8
	cat simbamon.8 |gzip >simbamon.8.gz

# list #######################################################################
list:
	@ls -l $(INSTALLED_FILES) || :

# phonies ####################################################################
.PHONY: install uninstall
