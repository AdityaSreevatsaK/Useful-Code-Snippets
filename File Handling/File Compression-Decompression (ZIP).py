import zipfile


# Compress files
def compress_files(zip_filename, *file_names):
    """
    Compress multiple files into a ZIP archive.

    This function creates a ZIP file and adds the specified files to it.

    Parameters:
    zip_filename (str): The name of the ZIP file to create.
    *file_names (str): The names of the files to compress.
    """
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for file in file_names:
            zip_file.write(file)


# Decompress files
def decompress_files(zip_filename, extract_folder):
    """
    Decompress a ZIP archive into a specified folder.

    This function extracts all files from the given ZIP file into the
    specified folder.

    Parameters:
    zip_filename (str): The name of the ZIP file to decompress.
    extract_folder (str): The folder where the files will be extracted.
    """
    with zipfile.ZipFile(zip_filename, 'r') as zip_file:
        zip_file.extractall(extract_folder)


compress_files('archive.zip', 'file1.txt', 'file2.txt')
decompress_files('archive.zip', './extracted')
