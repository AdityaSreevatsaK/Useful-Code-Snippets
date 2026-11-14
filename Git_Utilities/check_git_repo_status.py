"""Check the local checkout without interpreting Git failures as success."""

import subprocess


def is_git_repo_clean() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True,
        text=True, check=True, timeout=10,
    )
    return not result.stdout.strip()
