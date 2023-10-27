import httpx
import re
from tld import get_tld
from typing import Optional
from urllib.parse import urlparse, urlsplit
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


def is_http(url: str) -> bool:
    """
    Check if specified URL starts with http(s) scheme.
    """
    return url.startswith('http')


def is_toppage(url: str) -> bool:
    """
    Check if specified URL is the top page.
    """
    toppage = "{0.scheme}://{0.netloc}".format(urlsplit(url))
    return url == toppage or url == f"{toppage}/" or url == f"{toppage}/index.html"


def is_internal_link(link: str) -> bool:
    """
    Check if specified link is internal.
    """
    return link.startswith('#')


def get_robots_urls(client: httpx.Client, url: str) -> Optional[tuple[set[str], set[str]]]:
    """
    Get URLs in `robots.txt`.
    """
    allowed_urls = set()
    disallowed_urls = set()

    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url))
    robots_url = base_url + "/robots.txt"

    try:
        resp = client.get(robots_url)
    except:
        return None

    matches_allow = re.findall('Allow: (.*)', resp.text)
    for match in matches_allow:
        match = ''.join(match)
        if '*' not in match:
            allowed_urls.add(base_url + match)

    matches_disallow = re.findall('Disallow: (.*)', resp.text)
    for match in matches_disallow:
        match = ''.join(match)
        if '*' not in match:
            disallowed_urls.add(base_url + match)

    return allowed_urls, disallowed_urls


def parse_hostname(url: str) -> Optional[str]:
    """
    Get a hostname from URL
    """
    return urlparse(url).hostname


def parse_link_url(url: str, link: str) -> str:
    """
    Get a URL from a link
    """
    base_url = "{0.scheme}://{0.netloc}".format(urlsplit(url))
    link = f"/{link}" if link[0] != '/' else link 
    return f"{base_url}{link}" 


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
