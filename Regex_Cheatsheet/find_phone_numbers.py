import re


def find_phone_numbers(text: str) -> list:
    """
        Description:
            This function uses a regular expression to find all phone numbers consisting of exactly 10 digits within
            the provided text.

        Args:
            text (str): The input text string containing phone numbers.

        Returns:
            list: A list of strings, each representing a phone number found in the input text.
    """
    # Regular expression pattern to match phone numbers with exactly 10 digits
    pattern = r'\b\d{10}\b'
    return re.findall(pattern, text)


print(find_phone_numbers("Call me at 9876543210 or 1234567890."))
