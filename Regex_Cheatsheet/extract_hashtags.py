import re


def extract_hashtags(text: str) -> list:
    """
        Description:
            Extracts hashtags from a given text.

        Args:
            text (str): The input text containing hashtags.

        Returns:
            list: A list of extracted hashtags.
    """
    pattern = r'#\w+'
    return re.findall(pattern, text)


print(extract_hashtags("Loving the #MachineLearning and #AI trends!"))
