import shutil


def check_disk_usage(path="/"):
    """
    Description: Check the disk usage of the specified path.

    Args:
        path (str, optional): The path to check the disk usage for. Defaults to "/".

    Returns:
        (total, used, free): A tuple containing the total, used, and free disk space in bytes.
    """
    total, used, free = shutil.disk_usage(path)

    return total, used, free
