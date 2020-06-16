from configparser import ConfigParser
from pathlib import Path
from tuxmake.exceptions import InvalidToolchain


class Toolchain:
    def __init__(self, name):
        family = name.split("-")[0]
        conffile = Path(__file__).parent / "toolchain" / f"{family}.ini"
        if not conffile.exists():
            raise InvalidToolchain(name)
        config = ConfigParser()
        config.optionxform = str
        config.read(conffile)

        self.name = name
        self.makevars = config["makevars"]
