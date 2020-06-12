import sys
from tuxmake.cli import main as tuxmake


def test_basic_build(linux, home):
    tuxmake(str(linux))
    assert (home / ".cache/tuxmake/builds/1").exists()


def test_build_from_sys_argv(monkeypatch, mocker):
    build = mocker.patch("tuxmake.cli.build")
    monkeypatch.setattr(sys, "argv", ["tuxmake", "/path/to/linux"])
    tuxmake()
    build.assert_called_with(tree="/path/to/linux")


def test_build_from_sys_argv_default_tree_is_cwd(monkeypatch, mocker):
    build = mocker.patch("tuxmake.cli.build")
    monkeypatch.setattr(sys, "argv", ["tuxmake"])
    tuxmake()
    build.assert_called_with(tree=".")
