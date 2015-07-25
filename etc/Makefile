
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

.PHONY: install
install:
	install -d $(DESTDIR)/etc $(DESTDIR)/etc/logrotate.d
	install --owner=portage --group=portage --mode=0666 -d $(DESTDIR)/etc/gentoo-oam.d $(DESTDIR)/var/log/oam/old
	install --mode=0644 gentoo-oam.conf $(DESTDIR)/etc
	install --mode=0644 gentoo-oam.logrotate $(DESTDIR)/etc/logrotate.d/gentoo-oam
	install --mode=0644 officenet.conf $(DESTDIR)/etc/gentoo-oam.d
	install --mode=0644 weekly.conf $(DESTDIR)/etc/gentoo-oam.d
	install --mode=0644 monthly.conf $(DESTDIR)/etc/gentoo-oam.d
