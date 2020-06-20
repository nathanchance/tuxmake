O ?= $(CURDIR)
ARCH := $(shell uname -m)
VERSION := $(shell uname -r)

all:

include $(ARCH).mk
ARCHDIRNAME ?= $(ARCH)

.PHONY: vmlinux $(IMAGE) modules modules_install

all: vmlinux $(IMAGE)

define maybefail
	@if [ "$(filter $(1),$(FAIL))" = "$(1)" ]; then echo "Error: target $(FAIL) failed"; exit 1; fi
endef

$(IMAGE): $(O)/arch/$(ARCHDIRNAME)/boot/$(IMAGE)

vmlinux: $(O)/vmlinux

modules: $(O)/modules

$(O)/arch/$(ARCHDIRNAME)/boot/$(IMAGE): $(O)/vmlinux
	$(call maybefail,kernel)
	mkdir -p $$(dirname $@)
	touch $@

$(O)/vmlinux: $(O)/.config
	$(call maybefail,debugkernel)
	touch $@

$(O)/modules: $(O)/vmlinux
	$(call maybefail,modules)
	mkdir -p $@/lib/modules/$(VERSION)/kernel/fs/ext4
	touch    $@/lib/modules/$(VERSION)/kernel/fs/ext4/ext4.ko

modules_install: $(O)/modules
	mkdir -p $(INSTALL_MOD_PATH)
	cp -r $(O)/modules/lib $(INSTALL_MOD_PATH)/

defconfig:
	$(call maybefail,defconfig)
	mkdir -p $(O)
	touch $(O)/.config

clean:
	$(RM) -rf $(O)/arch/ $(O)/.config
