"""Explicit Fernet encryption helpers.

Keys are intentionally never generated or saved during module import.
Do not commit generated keys to a public repository.
"""

from pathlib import Path

from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """Generate a key that should be stored in a secure secrets manager."""
    return Fernet.generate_key()


def encrypt_file(source_path: str, output_path: str, key: bytes) -> None:
    """Encrypt file bytes using the supplied Fernet key."""
    source = Path(source_path)
    destination = Path(output_path)
    if source.resolve() == destination.resolve():
        raise ValueError("Source and destination must be different")
    payload = Fernet(key).encrypt(source.read_bytes())
    destination.write_bytes(payload)


def decrypt_file(source_path: str, output_path: str, key: bytes) -> None:
    """Decrypt a Fernet-encrypted file, or raise InvalidToken for a wrong key."""
    source = Path(source_path)
    destination = Path(output_path)
    if source.resolve() == destination.resolve():
        raise ValueError("Source and destination must be different")
    payload = Fernet(key).decrypt(source.read_bytes())
    destination.write_bytes(payload)
