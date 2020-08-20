import platform
from tuxmake.config import ConfigurableObject, split
from tuxmake.exceptions import UnsupportedArchitecture


class Architecture(ConfigurableObject):
    basedir = "arch"
    exception = UnsupportedArchitecture

    def __init_config__(self):
        self.targets = self.config["targets"]
        self.artifacts = self.config["artifacts"]
        self.makevars = self.config["makevars"]
        try:
            self.aliases = split(self.config["architecture"]["aliases"])
        except KeyError:
            self.aliases = []


class Native(Architecture):
    def __init__(self):
        name = platform.machine()
        super().__init__(name)
        self.makevars = {}


host_arch = Native()
