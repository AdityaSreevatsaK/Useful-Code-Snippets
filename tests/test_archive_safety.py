import io
import stat
import zipfile
from pathlib import Path

import pytest

from File_Handling.archive_safety import validate_archive
from File_Handling.compress_expand_files import decompress_files
from File_Handling.recursively_unzip_and_delete import unzip_and_delete


def archive_bytes(members):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in members:
            archive.writestr(name, data)
    return buffer.getvalue()


@pytest.mark.parametrize("name", ["../escape.txt", "/absolute.txt", "C:/windows.txt", "a/../../escape.txt"])
def test_rejects_unsafe_member_names(name):
    with zipfile.ZipFile(io.BytesIO(archive_bytes([(name, b"unsafe")]))) as archive:
        with pytest.raises(ValueError):
            validate_archive(archive)


def test_rejects_symlink():
    member = zipfile.ZipInfo("link.txt")
    member.create_system = 3
    member.external_attr = (stat.S_IFLNK | 0o777) << 16
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(member, "target")
    buffer.seek(0)
    with zipfile.ZipFile(buffer) as archive:
        with pytest.raises(ValueError):
            validate_archive(archive)


def test_rejects_compression_bomb():
    compressed = archive_bytes([("huge.txt", b"z" * (2 * 1024 * 1024))])
    with zipfile.ZipFile(io.BytesIO(compressed)) as archive:
        with pytest.raises(ValueError):
            validate_archive(archive)


def test_nested_extraction_and_cleanup(tmp_path):
    nested = archive_bytes([("books/novel.txt", b"hello")])
    (tmp_path / "outer.zip").write_bytes(archive_bytes([("inner.zip", nested)]))
    output = unzip_and_delete(str(tmp_path))
    assert len(output) == 1
    assert Path(output[0]).read_bytes() == b"hello"
    assert not (tmp_path / "outer.zip").exists()
    assert not (tmp_path / "inner.zip").exists()


def test_do_not_delete_archive_when_target_exists(tmp_path):
    (tmp_path / "keep.txt").write_text("existing")
    archive = tmp_path / "one.zip"
    archive.write_bytes(archive_bytes([("keep.txt", b"replace")]))
    with pytest.raises(ValueError):
        unzip_and_delete(str(tmp_path))
    assert archive.exists()
    assert (tmp_path / "keep.txt").read_text() == "existing"


def test_non_recursive_extraction_is_bounded(tmp_path):
    archive = tmp_path / "safe.zip"
    archive.write_bytes(archive_bytes([("sub/file.txt", b"ok")]))
    extracted = decompress_files(str(archive), str(tmp_path / "out"))
    assert len(extracted) == 1
    assert (tmp_path / "out" / "sub" / "file.txt").read_text() == "ok"
