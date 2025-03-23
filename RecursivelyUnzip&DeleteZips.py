import os
from zipfile import BadZipFile, ZipFile


def unzip_and_delete(folder_path):
    """
        Description: The unzip_and_delete function recursively scans a given folder for .zip files, extracts their
        contents to the same folder, and then deletes the original .zip file. It handles bad zip files and already
        deleted files gracefully, printing relevant messages during the process.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".zip"):
                zip_path = str(os.path.join(root, file))
                extract_path = root  # Extract to the same folder

                try:
                    # Unzip the file
                    with ZipFile(file=zip_path, mode="r") as zip_ref:
                        zip_ref.extractall(extract_path)
                        print(f"Extracted: {zip_path} to {extract_path}")

                    # Delete the .zip file
                    os.remove(zip_path)
                    print(f"Deleted: {zip_path}")

                    # Recursively check the extracted folder for more zips
                    unzip_and_delete(extract_path)

                except BadZipFile as bzp:
                    print(f"Bad Zip File: {zip_path}", bzp)
                except FileNotFoundError as file_error:
                    print("File deleted already.", file_error)


folder_to_scan = "Folder path"
unzip_and_delete(folder_to_scan)
