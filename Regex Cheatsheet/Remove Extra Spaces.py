import re


def remove_extra_spaces(text: str) -> str:
    """
        Description:
            This function uses a regular expression to replace multiple spaces with a single space and trims leading
            and trailing spaces.

        Args:
        text (str): The input text string containing extra spaces.

        Returns:
        str: A string with extra spaces removed.
    """
    # Regular expression pattern to match multiple spaces
    pattern = r'\s+'
    return re.sub(pattern, ' ', text).strip()


print(remove_extra_spaces("This   is  a    test."))
