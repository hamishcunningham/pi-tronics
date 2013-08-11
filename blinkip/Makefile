# Makefile for BlinkIP
# This code is copyright Hamish Cunningham and the University of Sheffield
# and is licenced under GPL 3 or any later version.

# vars #######################################################################
INSTALLED_FILES=\
/etc/blinkip.conf /usr/sbin/blinkip /etc/init.d/blinkipd \
/etc/default/blinkip /etc/rc?.d/*blinkipd /usr/share/man/man8/blinkip.8.gz
SUDO=/usr/bin/sudo

# help #######################################################################
help:
	@echo 'Makefile for BlinkIP                                          '
	@echo '                                                              '
	@echo 'Usage:                                                        '
	@echo '   make install                   installs the  BlinkIP daemon'
	@echo '   make uninstall                 removes the daemon          '
	@echo '   make list                      list installed files        '
	@echo '                                                              '

# install ####################################################################
install:
	SD=`which sudo` && \
          $$SD cp blinkip.conf          /etc                         && \
          $$SD cp blinkip               /usr/sbin                    && \
          $$SD cp blinkipd              /etc/init.d                  && \
          $$SD ln -fs /etc/blinkip.conf /etc/default/blinkip         && \
          $$SD cp blinkip.8.gz          /usr/share/man/man8          && \
          cd /etc/init.d && $$SD update-rc.d blinkipd defaults
	@echo 'BlinkIP installed: '
	@ls -l $(INSTALLED_FILES)

# uninstall ##################################################################
uninstall:
	@echo -n 'removing BlinkIP files: '
	@ls $(INSTALLED_FILES) || :
	sudo rm -f $(INSTALLED_FILES)
	@echo done

# manpage ####################################################################
blinkip.8: manpage.txt
	utils/txt2man -v "System Manager's Manual" -s 8 \
          -t 'blinkip' manpage.txt >blinkip.8
blinkip.8.gz: blinkip.8
	cat blinkip.8 |gzip >blinkip.8.gz

# list #######################################################################
list:
	@ls -l $(INSTALLED_FILES) || :

# phonies ####################################################################
.PHONY: install uninstall
