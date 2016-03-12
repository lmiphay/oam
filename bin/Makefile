
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

FILES=\
	oam \
	oam-mkset \
	oam-summary \
	oam-status

.PHONY: install
install:
	install -d $(DESTDIR)/usr/bin
	for i in $(FILES); do install $$i $(DESTDIR)/usr/bin || exit 1; done
