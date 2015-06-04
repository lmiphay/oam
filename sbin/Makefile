
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

FILES=\
	oam-clean \
	oam-edit-blocks \
	oam-edit-errors \
	oam-edit-glsa \
	oam-edit-merge \
	oam-edit-oam \
	oam-edit-sync \
	oam-emptytree \
	oam-expire \
	oam-fetch \
	oam-glsa \
	oam-kernel \
	oam-merge \
	oam-qcheck \
	oam-ranger \
	oam-sync \
	oam-unmask-write \
	oam-update \
	oam-weekly

.PHONY: install
install:
	install -d $(DESTDIR)/usr/sbin
	for i in $(FILES); do install $$i $(DESTDIR)/usr/sbin ; done
