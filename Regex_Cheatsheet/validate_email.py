import re


def validate_email(email: str) -> bool:
    """
        Description:
            Validate the format of an email address.

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email address is valid, False otherwise.
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))
