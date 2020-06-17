from tuxmake.build import BuildInfo


def test_status():
    info = BuildInfo("PASS")
    assert info.status == "PASS"


def test_fail():
    info = BuildInfo("FAIL")
    assert info.fail


def test_duration():
    info = BuildInfo("PASS", 1)
    assert info.duration == 1
