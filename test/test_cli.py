import argparse
import pytest
import sys
from tuxmake.cli import main as tuxmake


@pytest.fixture
def builds(home):
    return home / ".cache/tuxmake/builds"


@pytest.fixture(autouse=True)
def builder(mocker):
    return mocker.patch("tuxmake.cli.build")


def args(called):
    return argparse.Namespace(**called.call_args.kwargs)


def test_basic_build(linux, builder):
    tree = str(linux)
    tuxmake(tree)
    assert builder.call_args.kwargs == {"tree": tree}


def test_build_from_sys_argv(monkeypatch, builder):
    monkeypatch.setattr(sys, "argv", ["tuxmake", "/path/to/linux"])
    tuxmake()
    assert args(builder).tree == "/path/to/linux"


def test_build_from_sys_argv_default_tree_is_cwd(monkeypatch, builder):
    monkeypatch.setattr(sys, "argv", ["tuxmake"])
    tuxmake()
    assert args(builder).tree == "."


class TestTargets:
    def test_config(self, builder):
        tuxmake("--targets=config", "foo")
        args(builder).targets == ["config"]
        args(builder).tree == "foo"

    def test_config_multiple(self, builder):
        tuxmake("--targets=config,kernel", "foo")
        assert args(builder).targets == ["config", "kernel"]


class TestKConfig:
    def test_kconfig(self, builder):
        tuxmake("--kconfig=olddefconfig")
        assert args(builder).kconfig == ["olddefconfig"]
