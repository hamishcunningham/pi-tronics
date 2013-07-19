# Makefile for SimBaMon

# vars #######################################################################
X=y

# help #######################################################################
help:
	@echo 'Makefile for SimBaMon                                         '
	@echo '                                                              '
	@echo 'Usage:                                                        '
	@echo '   make install                   installs the SimBaMon daemon'
	@echo '                                                              '

# install ####################################################################
install:
	cp simbamon.conf         /etc
	cp simbamon              /usr/sbin
	cp simbamond             /etc/init.d
	ln -s /etc/simbamon.conf /etc/default/simbamon
	cd /etc/init.d &&        update-rc.d simbamond

# phonies ####################################################################
.PHONY: install
