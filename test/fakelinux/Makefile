O ?= $(CURDIR)
ARCH := $(shell uname -m)

all:

include $(ARCH).mk
ARCHDIRNAME ?= $(ARCH)

.PHONY: $(IMAGE)

all: $(IMAGE)

define maybefail
	@if [ "$(filter $(1),$(FAIL))" = "$(1)" ]; then echo "Error: target $(FAIL) failed"; exit 1; fi
endef

$(IMAGE): $(O)/arch/$(ARCHDIRNAME)/boot/$(IMAGE)

$(O)/arch/$(ARCHDIRNAME)/boot/$(IMAGE): $(O)/.config
	$(call maybefail,kernel)
	mkdir -p $$(dirname $@)
	touch $@

defconfig:
	$(call maybefail,defconfig)
	mkdir -p $(O)
	touch $(O)/.config

clean:
	$(RM) -rf $(O)/arch/ $(O)/.config
