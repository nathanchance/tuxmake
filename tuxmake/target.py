from configparser import ConfigParser
from pathlib import Path
from tuxmake.exceptions import UnsupportedTarget


class Target:
    def __init__(self, name, target_arch):
        conffile = Path(__file__).parent / "target" / f"{name}.ini"
        if not conffile.exists():
            raise UnsupportedTarget(name)
        config = ConfigParser()
        config.optionxform = str
        config.read(conffile)

        self.name = name
        self.description = config["target"].get("description")
        self.dependencies = config["target"].get("dependencies", [])
        self.make_args = config["target"].get("make_args", "").split()
        try:
            self.artifacts = config["artifacts"]
        except KeyError:
            key = target_arch.targets[name]
            value = target_arch.artifacts[key]
            self.artifacts = {key: value}

    def __str__(self):
        return self.name
