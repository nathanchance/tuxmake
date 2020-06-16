from pathlib import Path
import os
import shutil
import subprocess
from urllib.request import urlopen
from tuxmake.arch import Architecture
from tuxmake.toolchain import Toolchain
from tuxmake.output import get_new_output_dir
from tuxmake.exceptions import InvalidTarget


class defaults:
    target_arch = subprocess.check_output(["uname", "-m"], text=True).strip()
    toolchain = "gcc"
    kconfig = ["defconfig"]
    targets = ["config", "kernel"]


class Build:
    def __init__(self, source_tree, build_dir, output_dir):
        self.source_tree = source_tree
        self.build_dir = build_dir
        self.output_dir = output_dir
        self.arch = Architecture(defaults.target_arch)
        self.toolchain = Toolchain(defaults.toolchain)
        self.kconfig = defaults.kconfig
        self.artifacts = []

    def make(self, *args):
        subprocess.check_call(
            ["make", "--silent", f"O={self.build_dir}"] + self.makevars + list(args),
            cwd=self.source_tree,
        )

    @property
    def makevars(self):
        archvars = [f"{k}={v}" for k, v in self.arch.makevars.items()]
        toolchainvars = [
            f"{k}={v}".format(toolchain=self.toolchain.name, **self.arch.makevars)
            for k, v in self.toolchain.makevars.items()
        ]
        return archvars + toolchainvars

    def build(self, target):
        if target == "config":
            config = self.build_dir / ".config"
            for conf in self.kconfig:
                if conf.startswith("http://") or conf.startswith("https://"):
                    download = urlopen(conf)
                    with config.open("a") as f:
                        f.write(download.read().decode("utf-8"))
                elif Path(conf).exists():
                    with config.open("a") as f:
                        f.write(Path(conf).read_text())
                else:
                    self.make(conf)
        elif target == "kernel":
            kernel = self.arch.kernel
            self.make(kernel)
        else:
            raise InvalidTarget(f"Unsupported target: {target}")

    def copy_artifacts(self, target):
        if target == "kernel":
            dest = self.arch.kernel
        else:
            dest = target
        src = self.build_dir / self.arch.artifacts[dest]
        shutil.copy(src, Path(self.output_dir / dest))
        self.artifacts.append(dest)

    def cleanup(self):
        shutil.rmtree(self.build_dir)


def build(
    tree,
    target_arch=defaults.target_arch,
    toolchain=defaults.toolchain,
    kconfig=defaults.kconfig,
    targets=defaults.targets,
    output_dir=None,
):

    if output_dir is None:
        output_dir = get_new_output_dir()
    else:
        os.mkdir(output_dir)

    tmpdir = output_dir / "tmp"
    os.mkdir(tmpdir)

    builder = Build(tree, tmpdir, output_dir)
    builder.arch = Architecture(target_arch)
    builder.toolchain = Toolchain(toolchain)
    builder.kconfig = kconfig

    for target in targets:
        builder.build(target)

    for target in targets:
        builder.copy_artifacts(target)

    builder.cleanup()

    return builder
