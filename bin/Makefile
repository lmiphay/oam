
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

FILES=\
	oam-checkconfig \
	oam-emergelog \
	oam-genlop \
	oam-mkset \
	oam-summary \
	oam-status \
	oam-version \
	oam-watch

.PHONY: install
install:
	install -d $(DESTDIR)/usr/bin
	for i in $(FILES); do install $$i $(DESTDIR)/usr/bin || exit 1; done
