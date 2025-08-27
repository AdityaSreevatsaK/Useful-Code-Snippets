import os


def get_max_file_size(folder_path):
    """
        Description:
            The get_max_file_size function scans a given folder (including its subdirectories) and identifies the
            largest file based on size. It returns the file path and its size in bytes.

        Args:
            folder_path (str): The path to the folder to be scanned.

        Returns:
            tuple: A tuple containing the size of the largest file in bytes and its file path.
    """

    folder_path = folder_path.replace("\\", "/")
    max_size_value = 0
    max_file_value = None

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            if file_size > max_size_value:
                max_size_value = file_size
                max_file_value = file_path

    return max_size_value, max_file_value


# folder_to_scan = "Folder path"
# max_size, max_file = get_max_file_size(folder_to_scan)

# print(f"The largest file is: {max_file}")
# print(f"Size: {max_size / (1024 * 1024):.2f} MB")
