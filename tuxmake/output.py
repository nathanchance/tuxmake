from pathlib import Path
import os


def get_default_output_basedir():
    base = os.getenv("XDG_CACHE_HOME")
    if base:
        return Path(base) / "tuxmake" / "builds"
    else:
        return Path.home() / ".cache" / "tuxmake" / "builds"


def get_new_output_dir():
    base = get_default_output_basedir()
    existing = [int(f.name) for f in base.glob("[0-9]*")]
    if existing:
        new = str(max(existing) + 1)
    else:
        new = "1"
    new_dir = base / new
    new_dir.mkdir(parents=True)
    return new_dir
