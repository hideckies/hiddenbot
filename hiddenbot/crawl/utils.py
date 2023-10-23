import re
from tld import get_tld
from urllib.parse import urlparse
import validators
from validators import ValidationError


def is_url(url: str) -> bool:
    """
    Check if specified URL is valid or not.
    """
    result = validators.url(url)
    if isinstance(result, ValidationError):
        return False
    return result


def is_onion_url(url: str) -> bool:
    """
    Check if specified URL is an onion or not.
    """
    try:
        is_onion = get_tld(url) == 'onion'
    except:
        is_onion = False
    return is_onion


def get_hostname(url: str) -> str:
    """
    Get hostname from URL
    """
    return urlparse(url).hostname


def adjust_text(text: str) -> str:
    """
    Remove unexpected characters
    """
    text = text.strip()
    # Remove newline
    text = text.replace("\n", "")
    # Make multiple spaces to single space
    text = re.sub(' +', ' ', text)
    return text
