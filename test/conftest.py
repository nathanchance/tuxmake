import os
import pathlib
import pytest
import shutil


@pytest.fixture(autouse=True)
def home(mocker, tmp_path):
    h = tmp_path / "HOME"
    os.environ["HOME"] = str(h)
    return h


@pytest.fixture
def linux(tmp_path):
    src = pathlib.Path(__file__).parent / "fakelinux"
    dst = tmp_path / "linux"
    shutil.copytree(src, dst)
    return dst
