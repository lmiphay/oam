
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

.PHONY: install
install:
	install -d $(DESTDIR)/etc $(DESTDIR)/etc/cron.daily $(DESTDIR)/etc/cron.monthly
	install --mode=0640 --group=oam gentoo-oam.conf $(DESTDIR)/etc
	install --mode=0755 --group=root gentoo-oam.cron $(DESTDIR)/etc/cron.daily/gentoo-oam
	install --mode=0755 --group=root gentoo-oam-depclean-check.cron $(DESTDIR)/etc/cron.monthly/gentoo-oam-depclean-check
	install --mode=0640 --group=oam officenet.conf $(DESTDIR)/etc/gentoo-oam.d
	install --mode=0640 --group=oam weekly.conf $(DESTDIR)/etc/gentoo-oam.d
	install --mode=0640 --group=oam monthly.conf $(DESTDIR)/etc/gentoo-oam.d
	install --mode=0640 --group=oam sync.conf $(DESTDIR)/etc/gentoo-oam.d
