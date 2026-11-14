"""Boundary checks for the largest-file finder."""

import pytest

from File_Handling.get_max_file_size import get_max_file_size


def test_max_file_size_empty(tmp_path):
    assert get_max_file_size(str(tmp_path)) == (0, None)


def test_zero_byte_file_is_still_reported(tmp_path):
    source = tmp_path / "empty.txt"
    source.write_bytes(b"")
    assert get_max_file_size(str(tmp_path)) == (0, str(source))


def test_nested_largest_file(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "short.txt").write_bytes(b"x")
    large = tmp_path / "sub" / "big.txt"
    large.write_bytes(b"longer")
    assert get_max_file_size(str(tmp_path)) == (6, str(large))


def test_missing_directory_is_error(tmp_path):
    with pytest.raises(NotADirectoryError):
        get_max_file_size(str(tmp_path / "missing"))
