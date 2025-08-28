import re


def to_sentence_case(text: str) -> str:
    """
    Converts a given text string to sentence case.

    This function first converts the entire string to lowercase. Then, it
    capitalizes the first letter of the entire text and the first letter
    of every sentence that follows a sentence-ending punctuation mark
    (i.e., '.', '!', '?').

    Args:
        text: The input string to be converted.

    Returns:
        The text string in sentence case, or an empty string if the
        input is empty or not a string.
    """
    if not isinstance(text, str) or not text:
        return ""

    # 1. Convert the entire text to lower case, as per the request.
    lower_text = text.lower()

    # 2. Capitalize the letter following any sentence-ending punctuation.
    # We use re.sub with a function to perform the replacement.
    # The regex r'([.!?]\s+)([a-z])' finds:
    # - Group 1 ([.!?]\s+): A period, exclamation, or question mark,
    #   followed by one or more whitespace characters.
    # - Group 2 ([a-z]): The first lowercase letter of the next word.
    # The function then reconstructs the string, capitalizing the letter from group 2.
    def capitalize_after_punctuation(match):
        return match.group(1) + match.group(2).upper()

    interim_text = re.sub(r'([.!?]\s+)([a-z])', capitalize_after_punctuation, lower_text)

    # 3. Capitalize the very first letter of the entire text.
    # This loop finds the first alphabetical character and capitalizes it,
    # making the function robust to leading whitespace or symbols.
    for i, char in enumerate(interim_text):
        if char.isalpha():
            # Reconstruct the string with the first letter capitalized and return.
            return interim_text[:i] + char.upper() + interim_text[i + 1:]

    # If no alphabetical character is found in the string (e.g., "  . ! ?  "),
    # return the text as is.
    return interim_text

