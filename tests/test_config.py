from config import get_mode


def test_mode_from_ci_environment():
    assert get_mode() == "test"


def test_mutates_mode(monkeypatch):
    monkeypatch.setenv("MODE", "changed")
    assert get_mode() == "changed"


def test_mode_is_still_test():
    assert get_mode() == "test"
