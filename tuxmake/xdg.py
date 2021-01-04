import os
from pathlib import Path


def cache_home():
    home = os.getenv("XDG_CACHE_HOME")
    if home:
        return Path(home)
    else:
        return Path.home() / ".cache"
