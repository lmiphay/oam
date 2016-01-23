
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

SUBDIRS=\
	bin \
	etc \
	man \
	sbin

.PHONY: install
install:
	install -d $(DESTDIR)/etc $(DESTDIR)/etc/cron.daily
	install --owner=root --group=oam --mode=0750 -d $(DESTDIR)/etc/gentoo-oam.d
	install --owner=root --group=oam --mode=0770 -d $(DESTDIR)/var/log/oam
	install --owner=root --group=oam --mode=0770 -d $(DESTDIR)/var/log/oam/old
	touch $(DESTDIR)/var/log/oam/.keep_app-portage_gentoo-oam
	for i in $(SUBDIRS) ; do $(MAKE) $(MAKEOPTS) -C $$i install || exit 1; done
