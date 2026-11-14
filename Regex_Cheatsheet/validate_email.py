"""Simple structural validation of conventional ASCII email addresses."""

import re

_EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9_+%-]+(?:\.[A-Za-z0-9_+%-]+)*@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
)


def validate_email(email: str) -> bool:
    """Apply basic email syntax checks, not mail-server verification."""
    if not isinstance(email, str) or len(email) > 254:
        return False
    if not _EMAIL_PATTERN.fullmatch(email):
        return False
    domain = email.rsplit("@", 1)[-1]
    return len(domain.rsplit(".", 1)[-1]) >= 2
