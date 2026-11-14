"""Extract nested ZIPs safely. Never remove an archive after failed extraction."""

from pathlib import Path
from zipfile import ZipFile
import shutil

from File_Handling.archive_safety import MAX_TOTAL_BYTES, safe_destination, validate_archive


def unzip_and_delete(folder_path: str, max_depth: int = 5) -> list[str]:
    """Extract archives within folder_path and delete only successfully processed ZIPs.

    Limits total extraction to 100 MiB and at most five nested archive rounds.
    This utility is intended for untrusted uploads within a dedicated temporary directory.
    """
    base = Path(folder_path).resolve()
    if not base.is_dir():
        raise NotADirectoryError(folder_path)
    extracted: list[str] = []
    consumed = 0
    pending = sorted(base.rglob("*.zip"))
    round_number = 0
    while pending:
        if round_number >= max_depth:
            raise ValueError("Nested ZIP depth exceeded")
        next_round = []
        for archive_path in pending:
            if not archive_path.is_file():
                continue
            with ZipFile(archive_path) as archive:
                members = validate_archive(archive)
                planned = [(info, safe_destination(archive_path.parent, name)) for info, name in members]
                member_bytes = sum(info.file_size for info, _ in planned)
                if consumed + member_bytes > MAX_TOTAL_BYTES:
                    raise ValueError("Nested archives exceed total extracted size limit")
                for info, target in planned:
                    if not info.is_dir() and target.exists():
                        raise ValueError("Archive would overwrite an existing file")
                for info, target in planned:
                    if info.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with archive.open(info) as source, target.open("xb") as destination:
                            shutil.copyfileobj(source, destination)
                        extracted.append(str(target))
                        if target.suffix.lower() == ".zip":
                            next_round.append(target)
                consumed += member_bytes
            archive_path.unlink()
        pending = sorted(next_round)
        round_number += 1
    return [path for path in extracted if Path(path).exists() and Path(path).suffix.lower() != ".zip"]
