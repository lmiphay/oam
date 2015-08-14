
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
	install --owner=portage --group=portage --mode=0666 -d $(DESTDIR)/var/log/oam 
	touch $(DESTDIR)/var/log/oam/.keep_app-portage_gentoo-oam
	for i in $(SUBDIRS) ; do $(MAKE) $(MAKEOPTS) -C $$i install || exit 1; done
