
.PHONY: all
all:
	@echo "done"

.PHONY: check
check:
	@echo "done"

FILES=\
	oam-emergelog \
	oam-genlop \
	oam-uptime \
	oam-version \
	oam-watch

.PHONY: install
install:
	install -d $(DESTDIR)/usr/bin
	for i in $(FILES); do install $$i $(DESTDIR)/usr/bin ; done
