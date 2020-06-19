import subprocess
from tuxmake.config import ConfigurableObject
from tuxmake.exceptions import UnsupportedArchitecture


class Architecture(ConfigurableObject):
    basedir = "arch"
    exception = UnsupportedArchitecture

    def __init_config__(self):
        self.targets = self.config["targets"]
        self.artifacts = self.config["artifacts"]
        self.makevars = self.config["makevars"]


class Native(Architecture):
    def __init__(self):
        name = subprocess.check_output(["uname", "-m"], text=True).strip()
        super().__init__(name)
        self.makevars = {"CROSS_COMPILE": ""}
