
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
	sbin \
	share

.PHONY: install
install:
	install -d $(DESTDIR)/var/log/oam
	touch $(DESTDIR)/var/log/oam/.keep_app-portage_gentoo-oam
	for i in $(SUBDIRS) ; do $(MAKE) $(MAKEOPTS) -C $$i install ; done
