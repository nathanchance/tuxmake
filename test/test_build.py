import pytest
from tuxmake.build import build


@pytest.fixture
def output_dir(tmp_path):
    out = tmp_path / "output"
    return out


def test_build(linux, home):
    result = build(linux)
    assert "arch/x86/boot/bzImage" in result.artifacts
    assert (home / ".cache/tuxmake/builds/1/arch/x86/boot/bzImage").exists()


def test_build_with_output_dir(linux, output_dir):
    result = build(linux, output_dir=output_dir)
    assert "arch/x86/boot/bzImage" in result.artifacts
    assert (output_dir / "arch/x86/boot/bzImage").exists()
    assert result.output_dir == output_dir
