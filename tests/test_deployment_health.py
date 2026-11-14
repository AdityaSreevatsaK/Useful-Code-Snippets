"""Unit checks for the deployment health polling logic."""

from scripts.check_hf_space import check_space


def test_runtime_health_success(monkeypatch):
    monkeypatch.setattr("scripts.check_hf_space.read_json", lambda _: {
        "sha": "abc", "subdomain": "test-space",
        "runtime": {"stage": "RUNNING"},
    })
    monkeypatch.setattr("scripts.check_hf_space.http_healthy", lambda _: True)
    assert check_space("user/space", "abc", attempts=1, interval=0)


def test_wrong_commit_not_accepted(monkeypatch):
    monkeypatch.setattr("scripts.check_hf_space.read_json", lambda _: {
        "sha": "wrong", "runtime": {"stage": "RUNNING"},
    })
    assert not check_space("user/space", "expected", attempts=1, interval=0)


def test_runtime_failure(monkeypatch):
    monkeypatch.setattr("scripts.check_hf_space.read_json", lambda _: {
        "sha": "expected", "runtime": {"stage": "BUILD_ERROR"},
    })
    assert not check_space("user/space", "expected", attempts=1, interval=0)
