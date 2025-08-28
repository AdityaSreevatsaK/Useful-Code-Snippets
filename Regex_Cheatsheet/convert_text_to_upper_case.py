def to_upper_case(text: str) -> str:
    """
    Converts the input string to uppercase.

    This function first converts the input string to lowercase (to handle
    potential mixed-case inputs consistently) and then converts it to uppercase.

    Args:
        text: The input string to be converted.

    Returns:
        The uppercase version of the input string.
    """
    text = text.lower()
    return text.upper()
