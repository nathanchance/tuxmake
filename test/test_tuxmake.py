import pytest
import tuxmake


@pytest.fixture
def output_dir(mocker, tmp_path):
    get_new_output_dir = mocker.patch("tuxmake.get_new_output_dir")
    out = tmp_path / "output"
    get_new_output_dir.return_value = out
    out.mkdir()
    return out


def test_build(linux, home):
    build = tuxmake.build(linux)
    assert "arch/x86/boot/bzImage" in build.artifacts
    assert (home / ".cache/tuxmake/builds/1/arch/x86/boot/bzImage").exists()


def test_build_with_output_dir(linux, output_dir):
    build = tuxmake.build(linux)
    assert "arch/x86/boot/bzImage" in build.artifacts
    assert (output_dir / "arch/x86/boot/bzImage").exists()
