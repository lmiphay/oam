
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

.PHONY: install
install:
	install --mode=0640 --group=portage gentoo-oam.conf $(DESTDIR)/etc
	install --mode=0755 gentoo-oam.cron $(DESTDIR)/etc/cron.daily/gentoo-oam
	install --mode=0640 officenet.conf $(DESTDIR)/etc/gentoo-oam.d
	install --mode=0640 weekly.conf $(DESTDIR)/etc/gentoo-oam.d
	install --mode=0640 monthly.conf $(DESTDIR)/etc/gentoo-oam.d
	install --mode=0640 sync.conf $(DESTDIR)/etc/gentoo-oam.d
