"""Create and safely extract ZIP archives."""

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

from File_Handling.archive_safety import safe_destination, validate_archive


def compress_files(zip_filename: str, *file_names: str) -> None:
    with ZipFile(zip_filename, "w", ZIP_DEFLATED) as archive:
        for filename in file_names:
            archive.write(filename, arcname=Path(filename).name)


def decompress_files(zip_filename: str, extract_folder: str) -> list[str]:
    """Reject unsafe paths, symlinks and decompression bombs."""
    root = Path(extract_folder)
    root.mkdir(parents=True, exist_ok=True)
    extracted = []
    with ZipFile(zip_filename, "r") as archive:
        paths = [(info, safe_destination(root, name))
                 for info, name in validate_archive(archive)]
        for info, destination in paths:
            if destination.exists() and not info.is_dir():
                raise ValueError("Archive would overwrite an existing file")
        for info, destination in paths:
            if info.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
            else:
                destination.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as source, destination.open("xb") as output:
                    shutil.copyfileobj(source, output)
                extracted.append(str(destination))
    return extracted
