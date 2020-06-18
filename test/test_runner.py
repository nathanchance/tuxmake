import pytest

from tuxmake.build import Build
from tuxmake.runner import get_runner
from tuxmake.runner import NullRunner
from tuxmake.runner import DockerRunner


@pytest.fixture
def build(linux, tmp_path):
    b = Build(linux, tmp_path / "/tmp", tmp_path)
    return b


class TestGetRunner:
    def test_null_runner(self, build):
        build.docker = False
        assert isinstance(get_runner(build), NullRunner)

    def test_docker_runner(self, build):
        build.docker = True
        assert isinstance(get_runner(build), DockerRunner)


class TestNullRunner:
    def test_get_command_line(self):
        assert NullRunner().get_command_line(["date"]) == ["date"]


class TestDockerRunner:
    def test_docker_image(self, build, mocker):
        get_docker_image = mocker.patch("tuxmake.build.Build.get_docker_image")
        get_docker_image.return_value = "foobarbaz"
        runner = DockerRunner(build)
        assert runner.image == "foobarbaz"

    def test_prepare(self, build, mocker):
        check_call = mocker.patch("subprocess.check_call")
        DockerRunner(build).prepare()
        check_call.assert_called_with(["docker", "pull", mocker.ANY])

    def test_get_command_line(self, build):
        cmd = DockerRunner(build).get_command_line(["date"])
        assert cmd[0:2] == ["docker", "run"]
        assert cmd[-1] == "date"
