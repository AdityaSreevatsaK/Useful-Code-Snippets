import re


def extract_urls(text: str) -> list:
    """
    Description:
        Extract all URLs from a given text.

    Args:
        text (str): The input text containing URLs.

    Returns:
        list: A list of extracted URLs.
    """
    # Pattern to match URLs
    pattern = r'https?://(?:www\.)?\S+'
    return re.findall(pattern, text)


print(extract_urls("Visit https://example.com and http://test.com for details."))
