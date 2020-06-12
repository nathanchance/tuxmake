import argparse
import sys
from tuxmake.build import build


def main(*argv):
    if not argv:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="tuxmake")

    parser.add_argument(
        "tree", nargs="?", default=".", help="Tree to build (default: .)"
    )

    options = parser.parse_args(argv)
    result = build(tree=options.tree)
    print(f"I: build output in {result.output_dir}")
