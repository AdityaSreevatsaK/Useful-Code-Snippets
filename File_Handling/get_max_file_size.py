"""Find the largest regular file inside a directory tree."""

import os
from pathlib import Path


def get_max_file_size(folder_path: str) -> tuple[int, str | None]:
    """Return (byte_size, path); on an empty tree return (0, None)."""
    base = Path(folder_path)
    if not base.is_dir():
        raise NotADirectoryError(folder_path)
    max_size = 0
    max_file: str | None = None
    for root, dirs, files in os.walk(base, followlinks=False):
        dirs.sort()
        for name in sorted(files):
            path = Path(root) / name
            try:
                if not path.is_file() or path.is_symlink():
                    continue
                file_size = path.stat().st_size
            except OSError:
                # Files can be deleted while a directory scan is running.
                continue
            if max_file is None or file_size > max_size:
                max_size = file_size
                max_file = str(path)
    return max_size, max_file
