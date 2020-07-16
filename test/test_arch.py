import subprocess
from tuxmake.arch import Architecture
from tuxmake.arch import Native


class TestNative:
    def test_machine_name(self):
        m = subprocess.check_output(["uname", "-m"]).strip().decode("ascii")
        assert Native() == Architecture(m)


class TestAlias:
    def test_aarch64_is_an_alias_to_arm64(self):
        assert Architecture("aarch64") == Architecture("arm64")

    def test_alias_is_not_listed(self):
        assert "aarch64" not in Architecture.supported()
