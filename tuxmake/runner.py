import os
import subprocess


def get_runner(build):
    if build.docker:
        return DockerRunner(build)
    else:
        return NullRunner()


class NullRunner:
    def get_command_line(self, cmd):
        return cmd

    def prepare(self):
        pass


class DockerRunner:
    def __init__(self, build):
        self.build = build
        self.image = build.get_docker_image()

    def prepare(self):
        subprocess.check_call(["docker", "pull", self.image])

    def get_command_line(self, cmd):
        build = self.build
        source_tree = os.path.abspath(build.source_tree)
        build_dir = os.path.abspath(build.build_dir)

        uid = os.getuid()
        gid = os.getgid()
        return [
            "docker",
            "run",
            "--rm",
            f"--user={uid}:{gid}",
            f"--volume={source_tree}:{source_tree}",
            f"--volume={build_dir}:{build_dir}",
            f"--workdir={source_tree}",
            self.image,
        ] + cmd
