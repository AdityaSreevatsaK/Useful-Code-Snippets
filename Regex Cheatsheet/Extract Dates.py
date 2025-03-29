import re


def extract_dates(text: str) -> list:
    """
         Description:
            Extracts dates from the given text.

         Args:
             text (str): The input text containing dates.

         Returns:
             list: A list of extracted dates in the format DD-MM-YYYY or DD/MM/YYYY.
     """
    pattern = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b'
    return re.findall(pattern, text)


print(extract_dates("Important dates: 12-05-2023, 03/11/2022."))
