
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

FILES=\
	oam-clean \
	oam-depclean \
	oam-emptytree \
	oam-expire \
	oam-fetch \
	oam-flow \
	oam-glsa \
	oam-kernel \
	oam-merge \
	oam-qcheck \
	oam-sync \
	oam-unmask-write \
	oam-update \
	oam-weekly

.PHONY: install
install:
	install -d $(DESTDIR)/usr/sbin
	for i in $(FILES); do install $$i $(DESTDIR)/usr/sbin ; done
