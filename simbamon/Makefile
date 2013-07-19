# Makefile for SimBaMon
# This code is copyright Hamish Cunningham and the University of Sheffield
# and is licenced under GPL 3 or any later version.

# vars #######################################################################
INSTALLED_FILES=\
/etc/simbamon.conf /usr/sbin/simbamon /etc/init.d/simbamond \
/etc/default/simbamon /etc/rc?.d/*simbamond
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
          $$SD cp simbamon.conf         /etc                          && \
          $$SD cp simbamon              /usr/sbin                     && \
          $$SD cp simbamond             /etc/init.d                   && \
          $$SD ln -fs /etc/simbamon.conf /etc/default/simbamon        && \
          cd /etc/init.d && $$SD update-rc.d simbamond defaults
	@echo -n 'SimBaMod installed: '
	@ls -l $(INSTALLED_FILES)

# uninstall ##################################################################
uninstall:
	@echo -n 'removing SimBaMod files: '
	@ls $(INSTALLED_FILES) || :
	sudo rm -f $(INSTALLED_FILES)
	@echo done

# list #######################################################################
list:
	@ls -l $(INSTALLED_FILES) || :

# phonies ####################################################################
.PHONY: install uninstall
