from configparser import ConfigParser
from pathlib import Path


class Architecture:
    def __init__(self, arch):
        conffile = Path(__file__).parent / "arch" / f"{arch}.ini"
        config = ConfigParser()
        config.read(conffile)

        self.kernel = config["targets"]["kernel"]

        self.artifacts = []
        for target, artifact in config["artifacts"].items():
            self.artifacts.append(artifact)
