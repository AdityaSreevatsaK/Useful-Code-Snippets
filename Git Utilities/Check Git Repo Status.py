import subprocess


def is_git_repo_clean():
    result = subprocess.run(['git', 'status', '--porcelain'], stdout=subprocess.PIPE)
    return result.stdout.decode().strip() == ''


if is_git_repo_clean():
    print("Repo is clean ✅")
else:
    print("⚠️⚠️⚠️ Repo has uncommitted changes!")
