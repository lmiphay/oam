
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

.PHONY: install
install:
	install -d $(DESTDIR)/usr/sbin \
	$(DESTDIR)/etc $(DESTDIR)/etc/logrotate.d \
	$(DESTDIR)/var/log/oam/
	install gentoo-oam.conf $(DESTDIR)/etc
	install oam-fetch $(DESTDIR)/usr/sbin
	install oam-glsa $(DESTDIR)/usr/sbin
	install oam-qcheck $(DESTDIR)/usr/sbin
	install oam-sync $(DESTDIR)/usr/sbin
	install oam-unmask-write $(DESTDIR)/usr/sbin
	install oam-update $(DESTDIR)/usr/sbin
	install oam-watch $(DESTDIR)/usr/sbin
	install oam-weekly $(DESTDIR)/usr/sbin
	install gentoo-oam.logrotate $(DESTDIR)/etc/logrotate.d/gentoo-oam
	touch $(DESTDIR)/var/log/oam/.keep_app-portage_gentoo-oam
