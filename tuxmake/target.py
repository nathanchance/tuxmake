from pathlib import Path
import shlex
import urllib.request

from tuxmake.config import ConfigurableObject
from tuxmake.exceptions import UnsupportedTarget


def supported_targets():
    return Target.supported()


def create_target(name, build):
    cls = (name == "config") and Config or Target
    return cls(name, build)


class Target(ConfigurableObject):
    basedir = "target"
    exception = UnsupportedTarget

    def __init__(self, name, build):
        self.build = build
        self.target_arch = build.target_arch
        super().__init__(name)

    def __init_config__(self):
        self.description = self.config["target"].get("description")
        self.dependencies = self.config["target"].get("dependencies", "").split()
        self.make_args = self.__split_cmds__("target", "make_args") or [[]]
        self.preconditions = self.__split_cmds__("target", "preconditions")
        self.extra_commands = self.__split_cmds__("target", "extra_commands")
        try:
            self.artifacts = self.config["artifacts"]
        except KeyError:
            key = self.target_arch.targets[self.name]
            value = self.target_arch.artifacts[key]
            self.artifacts = {key: value}

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return str(self) == str(other)

    def __split_cmds__(self, section, item):
        s = self.config[section].get(item)
        if not s:
            return []
        result = [[]]
        for item in shlex.split(s):
            if item == "&&":
                result.append([])
            else:
                result[-1].append(item)
        return result

    def prepare(self):
        pass


class Config(Target):
    def __init_config__(self):
        super().__init_config__()
        self.make_args = []

    def prepare(self):
        config = self.build.build_dir / ".config"
        conf = self.build.kconfig
        if conf.startswith("http://") or conf.startswith("https://"):
            download = urllib.request.urlopen(conf)
            with config.open("w") as f:
                f.write(download.read().decode("utf-8"))
        elif Path(conf).exists():
            with config.open("w") as f:
                f.write(Path(conf).read_text())
        else:
            self.build.make(conf)
