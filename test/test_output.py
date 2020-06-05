from tuxmake.output import get_default_output_basedir
from tuxmake.output import get_new_output_dir


def test_default_output_basedir_xdg_cache_home(mocker, tmp_path):
    getenv = mocker.patch("os.getenv")
    getenv.return_value = str(tmp_path)
    assert get_default_output_basedir() == (tmp_path / "tuxmake" / "builds")
    getenv.assert_called_with("XDG_CACHE_HOME")


def test_default_output_basedir(mocker, tmp_path):
    home = mocker.patch("pathlib.Path.home")
    home.return_value = tmp_path
    assert get_default_output_basedir() == (tmp_path / ".cache/tuxmake/builds")


def test_get_new_output_dir(mocker, tmp_path):
    basedir = mocker.patch("tuxmake.output.get_default_output_basedir")
    basedir.return_value = tmp_path
    output_dir = get_new_output_dir()
    assert output_dir.name == "1"


def test_get_new_output_dir_2(mocker, tmp_path):
    basedir = mocker.patch("tuxmake.output.get_default_output_basedir")
    basedir.return_value = tmp_path
    get_new_output_dir()
    dir2 = get_new_output_dir()
    assert dir2.name == "2"
