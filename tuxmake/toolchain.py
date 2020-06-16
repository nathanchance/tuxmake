from configparser import ConfigParser
from pathlib import Path


class Toolchain:
    def __init__(self, name):
        family = name.split("-")[0]
        conffile = Path(__file__).parent / "toolchain" / f"{family}.ini"
        config = ConfigParser()
        config.optionxform = str
        config.read(conffile)

        self.name = name
        self.makevars = config["makevars"]
