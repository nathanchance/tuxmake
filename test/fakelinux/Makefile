O ?= $(CURDIR)
ARCH := $(shell uname -m)

all:

include $(ARCH).mk
ARCHDIRNAME ?= $(ARCH)

.PHONY: $(IMAGE)

all: $(IMAGE)

$(IMAGE): $(O)/arch/$(ARCHDIRNAME)/boot/$(IMAGE)

$(O)/arch/$(ARCHDIRNAME)/boot/$(IMAGE): $(O)/.config
	mkdir -p $$(dirname $@)
	touch $@

defconfig:
	mkdir -p $(O)
	touch $(O)/.config

clean:
	$(RM) -rf $(O)/arch/ $(O)/.config
