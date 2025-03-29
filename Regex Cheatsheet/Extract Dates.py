import re


def extract_dates(text: str) -> list:
    """
    Description:
        Extract dates from a given text string.

    This function uses a regular expression to find all dates in the format
    DD-MM-YYYY or DD/MM/YYYY within the provided text.

    Parameters:
    text (str): The input text string containing dates.

    Returns:
    list: A list of strings, each representing a date found in the input text.
    """
    # Regular expression pattern to match dates in the format DD-MM-YYYY or DD/MM/YYYY
    pattern = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b'
    return re.findall(pattern, text)


print(extract_dates("Important dates: 12-05-2023, 03/11/2022."))
