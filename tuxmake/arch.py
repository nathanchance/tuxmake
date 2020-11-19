import platform
from tuxmake.config import ConfigurableObject
from tuxmake.exceptions import UnsupportedArchitecture


class Architecture(ConfigurableObject):
    basedir = "arch"
    exception = UnsupportedArchitecture
    config_aliases = {"aarch64": "arm64", "amd64": "x86_64"}

    def __init_config__(self):
        self.targets = self.config["targets"]
        self.artifacts = self.config["artifacts"]
        self.makevars = self.config["makevars"]
        self.aliases = [k for k, v in self.config_aliases.items() if v == self.name]


class Native(Architecture):
    def __init__(self):
        name = platform.machine()
        super().__init__(name)
        self.makevars = {}


host_arch = Native()
