from typing import Optional, Type
from configparser import ConfigParser
from pathlib import Path


class ConfigurableObject:
    basedir: Optional[str] = None
    exception: Optional[Type[Exception]] = None

    def __init__(self, name):
        commonconf = Path(__file__).parent / self.basedir / "common.ini"
        conffile = Path(__file__).parent / self.basedir / f"{name}.ini"
        if not conffile.exists():
            raise self.exception(name)
        self.name = name
        self.config = ConfigParser()
        self.config.optionxform = str
        self.config.read(commonconf)
        self.config.read(conffile)
        self.__init_config__()

    def __init_config__(self):
        raise NotImplementedError

    @classmethod
    def supported(cls):
        files = (Path(__file__).parent / cls.basedir).glob("*.ini")
        return [
            str(f.name).replace(".ini", "") for f in files if f.name != "common.ini"
        ]
