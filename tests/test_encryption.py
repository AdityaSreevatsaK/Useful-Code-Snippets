from cryptography.fernet import InvalidToken
import pytest

from File_Handling.encrypt_decrypt_files import (
    decrypt_file, encrypt_file, generate_key,
)


def test_encryption_round_trip(tmp_path):
    source = tmp_path / "clear.txt"
    encrypted = tmp_path / "encrypted.bin"
    restored = tmp_path / "restored.txt"
    source.write_text("secret data", encoding="utf-8")
    key = generate_key()
    encrypt_file(str(source), str(encrypted), key)
    assert encrypted.read_bytes() != source.read_bytes()
    decrypt_file(str(encrypted), str(restored), key)
    assert restored.read_bytes() == source.read_bytes()


def test_rejects_wrong_key(tmp_path):
    source = tmp_path / "plain"
    encrypted = tmp_path / "encrypted"
    source.write_bytes(b"contents")
    encrypt_file(str(source), str(encrypted), generate_key())
    with pytest.raises(InvalidToken):
        decrypt_file(str(encrypted), str(tmp_path / "bad"), generate_key())


def test_rejects_in_place_encrypt(tmp_path):
    source = tmp_path / "plain"
    source.write_bytes(b"contents")
    with pytest.raises(ValueError):
        encrypt_file(str(source), str(source), generate_key())
