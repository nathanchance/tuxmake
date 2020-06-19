from pathlib import Path
import datetime
import os
import shutil
import subprocess
import time
from urllib.request import urlopen
from tuxmake.arch import Architecture, Native
from tuxmake.toolchain import Toolchain, NoExplicitToolchain
from tuxmake.output import get_new_output_dir
from tuxmake.runner import get_runner
from tuxmake.exceptions import UnsupportedTarget
from tuxmake.exceptions import UnrecognizedSourceTree


class defaults:
    kconfig = ["defconfig"]
    targets = ["config", "kernel"]
    jobs = int(subprocess.check_output(["nproc"], text=True)) * 2


class BuildInfo:
    def __init__(self, status, duration=None):
        self.status = status
        self.duration = duration

    @property
    def fail(self):
        return self.status == "FAIL"


class Build:
    def __init__(
        self,
        source_tree,
        *,
        output_dir=None,
        target_arch=None,
        toolchain=None,
        kconfig=defaults.kconfig,
        targets=defaults.targets,
        jobs=defaults.jobs,
        docker=False,
        docker_image=None,
    ):
        self.source_tree = source_tree

        if output_dir is None:
            self.output_dir = get_new_output_dir()
        else:
            self.output_dir = output_dir
            os.mkdir(self.output_dir)

        self.build_dir = self.output_dir / "tmp"
        os.mkdir(self.build_dir)

        self.target_arch = target_arch and Architecture(target_arch) or Native()
        self.toolchain = toolchain and Toolchain(toolchain) or NoExplicitToolchain()

        self.kconfig = kconfig
        self.targets = targets
        self.jobs = jobs

        self.docker = docker
        self.docker_image = docker_image

        self.artifacts = ["build.log"]
        self.runner = None
        self.__logger__ = None
        self.status = {}

    def validate(self):
        source = Path(self.source_tree)
        files = [str(f.name) for f in source.glob("*")]
        if "Makefile" in files and "Kconfig" in files and "Kbuild" in files:
            return
        raise UnrecognizedSourceTree(source.absolute())

    def prepare(self):
        self.runner = get_runner(self)
        self.runner.prepare()

    def make(self, *args):
        cmd = (
            ["make", "--silent", f"--jobs={self.jobs}", f"O={self.build_dir}"]
            + self.makevars
            + list(args)
        )

        if self.runner:
            final_cmd = self.runner.get_command_line(cmd)
        else:
            final_cmd = cmd

        self.log(" ".join(cmd))
        subprocess.check_call(
            final_cmd,
            cwd=self.source_tree,
            stdout=self.logger.stdin,
            stderr=subprocess.STDOUT,
        )

    @property
    def logger(self):
        if not self.__logger__:
            self.__logger__ = subprocess.Popen(
                ["tee", str(self.output_dir / "build.log")], stdin=subprocess.PIPE
            )
        return self.__logger__

    def log(self, *stuff):
        subprocess.call(["echo"] + list(stuff), stdout=self.logger.stdin)

    @property
    def makevars(self):
        return [f"{k}={v}" for k, v in self.environment.items() if v]

    @property
    def environment(self):
        v = {}
        v.update(self.target_arch.makevars)
        v.update(self.toolchain.expand_makevars(self.target_arch))
        return v

    def build(self, target):
        start = time.time()
        try:
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
            elif target == "debugkernel":
                self.make(self.target_arch.debugkernel)
            elif target == "kernel":
                self.make()
            else:
                raise UnsupportedTarget(target)
            self.status[target] = BuildInfo("PASS")
        except subprocess.CalledProcessError:
            self.status[target] = BuildInfo("FAIL")
        finish = time.time()
        self.status[target].duration = datetime.timedelta(seconds=finish - start)

    def copy_artifacts(self, target):
        if self.status[target].fail:
            return
        if target == "kernel":
            dest = self.target_arch.kernel
        elif target == "debugkernel":
            dest = self.target_arch.debugkernel
        else:
            dest = target
        src = self.build_dir / self.target_arch.artifacts[dest]
        shutil.copy(src, Path(self.output_dir / dest))
        self.artifacts.append(dest)

    @property
    def passed(self):
        s = [info.fail for info in self.status.values()]
        return s and True not in set(s)

    @property
    def failed(self):
        s = [info.fail for info in self.status.values()]
        return s and True in set(s)

    def cleanup(self):
        self.logger.terminate()
        shutil.rmtree(self.build_dir)

    def get_docker_image(self):
        return self.toolchain.get_docker_image(self.target_arch)

    def run(self):
        self.validate()

        self.prepare()

        for target in self.targets:
            self.build(target)

        for target in self.targets:
            self.copy_artifacts(target)

        self.cleanup()


def build(tree, **kwargs):
    builder = Build(tree, **kwargs)
    builder.run()
    return builder
