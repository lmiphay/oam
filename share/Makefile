
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

.PHONY: install
install:
	install -d $(DESTDIR)/usr/share/gentoo-oam
	install --mode=0644 gentoo-oam-functions.sh $(DESTDIR)/usr/share/gentoo-oam
	install --mode=0644 gentoo-oam-multitail.conf $(DESTDIR)/usr/share/gentoo-oam
	install --mode=0644 oam-watch.help $(DESTDIR)/usr/share/gentoo-oam
	install --mode=0644 summary.jinja2 $(DESTDIR)/usr/share/gentoo-oam
