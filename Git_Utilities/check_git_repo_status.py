import subprocess


def is_git_repo_clean():
    """
    Description:
        Check if the current Git repository is clean (i.e., has no uncommitted changes).
        This function runs the `git status --porcelain` command to determine the status
        of the repository.

    Returns:
        bool: True if the repository is clean, False otherwise.
    """
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    return result.stdout.decode().strip() == ''

