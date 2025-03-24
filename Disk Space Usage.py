import shutil


def check_disk_usage(path="/"):
    """
    Description: Check the disk usage of the specified path.

    Args:
        path (str, optional): The path to check the disk usage for. Defaults to "/".

    Returns:
        None
    """
    total, used, free = shutil.disk_usage(path)
    print(f"Total: {total // (1024 ** 3)} GB")
    print(f"Used: {used // (1024 ** 3)} GB")
    print(f"Free: {free // (1024 ** 3)} GB")


# Folder path to be checked.
check_disk_usage(path="C:/")
