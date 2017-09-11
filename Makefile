
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

.PHONY: install
install:
	install -d $(DESTDIR)/etc
	install --owner=root --group=oam --mode=0750 -d $(DESTDIR)/etc/oam
	install --owner=root --group=oam --mode=0750 -d $(DESTDIR)/etc/conf.d
	install --owner=root --group=oam --mode=0770 -d $(DESTDIR)/var/log/oam
	install --owner=root --group=oam --mode=0770 -d $(DESTDIR)/var/log/oam/old
	install --owner=root --group=oam --mode=0770 -d $(DESTDIR)/var/db/oam
	touch $(DESTDIR)/var/log/oam/.keep_app-portage_oam
	touch $(DESTDIR)/var/db/oam/.keep_app-portage_oam
