
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

.PHONY: install
install:
	install -d $(DESTDIR)/usr/sbin
	install oam-fetch $(DESTDIR)/usr/sbin
	install oam-qcheck $(DESTDIR)/usr/sbin
	install oam-sync $(DESTDIR)/usr/sbin
	install oam-update $(DESTDIR)/usr/sbin
	install oam-weekly $(DESTDIR)/usr/sbin

