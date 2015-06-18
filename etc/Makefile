
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

.PHONY: install
install:
	install -d $(DESTDIR)/etc $(DESTDIR)/etc/gentoo-oam.d $(DESTDIR)/etc/logrotate.d $(DESTDIR)/var/log/oam/old
	install --mode=0644 gentoo-oam.conf $(DESTDIR)/etc
	install --mode=0644 gentoo-oam.logrotate $(DESTDIR)/etc/logrotate.d/gentoo-oam
