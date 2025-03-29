import os
from zipfile import BadZipFile, ZipFile


def unzip_and_delete(folder_path):
    """
        Description:
            This function recursively unzips files in the specified folder and deletes the original .zip files.
            If a .zip file contains another .zip file, it will continue to unzip until there are no more .zip files.

        Args:
            folder_path (str): The path to the folder to be scanned for .zip files.

        Returns:
            None
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
