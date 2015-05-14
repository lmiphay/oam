
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
	$(DESTDIR)/usr/share/gentoo-oam \
	$(DESTDIR)/var/log/oam/ \
	$(DESTDIR)/usr/share/man/man8
	install gentoo-oam.conf $(DESTDIR)/etc
	install gentoo-oam-functions.sh $(DESTDIR)/usr/share/gentoo-oam
	install gentoo-oam-multitail.conf $(DESTDIR)/usr/share/gentoo-oam
	install oam-emptytree $(DESTDIR)/usr/sbin
	install oam-fetch $(DESTDIR)/usr/sbin
	install oam-glsa $(DESTDIR)/usr/sbin
	install oam-qcheck $(DESTDIR)/usr/sbin
	install oam-genlop-current $(DESTDIR)/usr/sbin
	install oam-merge $(DESTDIR)/usr/sbin
	install oam-sync $(DESTDIR)/usr/sbin
	install oam-unmask-write $(DESTDIR)/usr/sbin
	install oam-update $(DESTDIR)/usr/sbin
	install oam-uptime $(DESTDIR)/usr/sbin
	install oam-version $(DESTDIR)/usr/sbin
	install oam-watch $(DESTDIR)/usr/sbin
	install oam-weekly $(DESTDIR)/usr/sbin
	install gentoo-oam.logrotate $(DESTDIR)/etc/logrotate.d/gentoo-oam
	install gentoo-oam.8 $(DESTDIR)/usr/share/man/man8/
	touch $(DESTDIR)/var/log/oam/.keep_app-portage_gentoo-oam
