"""Safety checks for ZIP archives supplied by users."""

from pathlib import Path
from zipfile import ZipFile, ZipInfo
import stat

MAX_FILES = 200
MAX_MEMBER_BYTES = 40 * 1024 * 1024
MAX_TOTAL_BYTES = 100 * 1024 * 1024
MAX_RATIO = 200


def safe_member_name(info: ZipInfo) -> str:
    """Reject absolute, parent-traversal, or symlink archive members."""
    name = info.filename.replace("\\", "/")
    if not name or name.startswith("/") or name.startswith("//"):
        raise ValueError("Unsafe archive member path")
    segments = name.rstrip("/").split("/")
    if not segments or any(part in ("", ".", "..") for part in segments):
        raise ValueError("Unsafe archive member path")
    if ":" in segments[0] or "\x00" in name:
        raise ValueError("Unsafe archive member path")
    if stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK:
        raise ValueError("Archive contains a symbolic link")
    return "/".join(segments)


def validate_archive(archive: ZipFile) -> list[tuple[ZipInfo, str]]:
    """Validate every entry before reading/extracting any member."""
    infos = archive.infolist()
    if len(infos) > MAX_FILES:
        raise ValueError("Archive contains too many entries")
    total = 0
    names = set()
    validated = []
    for info in infos:
        name = safe_member_name(info)
        if name in names:
            raise ValueError("Archive contains duplicate paths")
        names.add(name)
        total += info.file_size
        if info.file_size > MAX_MEMBER_BYTES or total > MAX_TOTAL_BYTES:
            raise ValueError("Archive exceeds decompressed size limit")
        if info.file_size > 1024 * 1024 and info.file_size > MAX_RATIO * max(1, info.compress_size):
            raise ValueError("Archive has an unsafe compression ratio")
        if info.flag_bits & 0x1:
            raise ValueError("Encrypted ZIP entries are not supported")
        validated.append((info, name))
    return validated


def safe_destination(root: str | Path, name: str) -> Path:
    """Resolve a validated member name inside an extraction directory."""
    base = Path(root).resolve()
    target = (base / name).resolve()
    if not target.is_relative_to(base) or target == base:
        raise ValueError("Archive extraction would escape the destination")
    return target
