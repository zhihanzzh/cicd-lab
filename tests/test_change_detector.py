import pytest

from scripts.change_detector import classify


@pytest.mark.parametrize(
    "changed_files, expected_flags",
    [
        (["docs/README.md"], (False, False, False, False, False)),
        (
            ["backend/api.py", "scripts/build_release.py"],
            (True, False, False, False, True),
        ),
        (["Dockerfile"], (False, False, False, True, False)),
        (
            ["training/model.py", "infra/k8s/job.yaml"],
            (False, True, True, False, False),
        ),
        (
            ["shared/config.py", "infra/k8s/job.yaml", "docs/README.md"],
            (True, True, True, False, False),
        ),
        (
            ["training/old.py", "backend/new.py"],
            (True, True, False, False, False),
        ),
        (["pyproject.toml"], (True, True, False, False, False)),
        ([], (False, False, False, False, False)),
        (
            ["scripts/build_release.py", "backend/api.py"],
            (True, False, False, False, True),
        ),
        (
            ["backend_extra/api.py", "docs_extra/README.md", "nested/Dockerfile"],
            (False, False, False, False, True),
        ),
    ],
    ids=[
        "docs-only",
        "backend-and-unknown",
        "dockerfile",
        "training-and-infra",
        "shared-infra-and-docs",
        "rename-like-paths",
        "pyproject",
        "empty",
        "unknown-before-backend",
        "unmatched-path-boundaries",
    ],
)
def test_classify(changed_files, expected_flags):
    keys = ("backend", "training", "infra", "docker", "unknown")
    expected = dict(zip(keys, expected_flags))

    result = classify(changed_files)

    assert result == expected
    assert all(type(value) is bool for value in result.values())
