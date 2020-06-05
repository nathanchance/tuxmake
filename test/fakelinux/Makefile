O ?= $(CURDIR)

bzImage: $(O)/arch/x86/boot/bzImage

$(O)/arch/x86/boot/bzImage: $(O)/.config
	mkdir -p $$(dirname $@)
	touch $@

defconfig:
	touch $(O)/.config

clean:
	$(RM) -rf $(O)/arch/
