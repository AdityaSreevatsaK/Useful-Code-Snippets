"""Coverage for every regex utility and text conversion in the dashboard."""

import pytest

from Regex_Cheatsheet.convert_text_to_lower_case import to_lower_case
from Regex_Cheatsheet.convert_text_to_sentence_case import to_sentence_case
from Regex_Cheatsheet.convert_text_to_upper_case import to_upper_case
from Regex_Cheatsheet.extract_dates import extract_dates
from Regex_Cheatsheet.extract_hashtags import extract_hashtags
from Regex_Cheatsheet.extract_urls import extract_urls
from Regex_Cheatsheet.find_phone_numbers import find_phone_numbers
from Regex_Cheatsheet.remove_extra_spaces import remove_extra_spaces
from Regex_Cheatsheet.validate_email import validate_email


def test_text_case_tools():
    assert to_lower_case("HeLLo") == "hello"
    assert to_upper_case("HeLLo") == "HELLO"
    assert to_sentence_case("HELLO THERE. HOW ARE YOU? fine!") == (
        "Hello there. How are you? Fine!"
    )
    assert to_sentence_case("") == ""


def test_extractors():
    assert extract_dates("Dates: 14/11/2026 and 02-01-2027") == [
        "14/11/2026", "02-01-2027",
    ]
    assert extract_hashtags("#open_source #ai") == ["#open_source", "#ai"]
    assert extract_urls("visit https://example.com/test") == ["https://example.com/test"]
    assert find_phone_numbers("Call 1234567890, not 12345") == ["1234567890"]
    assert remove_extra_spaces("  hello   world \n ") == "hello world"


@pytest.mark.parametrize("email", ["alice@example.com", "first.last+tag@sub.example.co.uk"])
def test_valid_email(email):
    assert validate_email(email)


@pytest.mark.parametrize("email", [
    "", "hello", "@example.com", "alice..bob@example.com",
    "alice@-example.com", "alice@example..com", "alice@example.com.",
    "alice@example.c", "alice@example.com/evil",
])
def test_invalid_email(email):
    assert not validate_email(email)
