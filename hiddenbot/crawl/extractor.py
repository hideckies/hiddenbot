from bs4 import BeautifulSoup
import re
from typing import Optional
from .utils import (
    adjust_text, parse_hostname, parse_link_url,
    is_http, is_internal_link, is_onion_url, is_url
)


def extract_meta_refresh(s: BeautifulSoup) -> Optional[str]:
    """
    Extract redirect URL in the meta 'http-equiv=refresh'.

    Parameters
    ----------------------------------
    s: BeautifulSoup
        Used for scraping.
    """
    # meta_refresh = s.find('meta', attrs={'http-equiv': 'Refresh'})
    meta_refresh = s.find('meta', attrs={'http-equiv': re.compile('^refresh$', re.I)})
    if meta_refresh is None:
        return None
    
    content = meta_refresh.get('content')
    matched = re.search('url=(.+\.onion.*)', content)
    if matched is None:
        return None

    return matched.group(1)


def extract_site_info(
    s: BeautifulSoup,
    url: str,
    max_content_length: int,
) -> Optional[tuple[str, str, str]]:
    """
    Extract the site title, description and content.

    Parameters
    ---------------------------------
    s: BeautifulSoup
        Used for scraping.
    url: str
        URL which is scraped.
    max_content_words: int
        Miximum number of words in content to extract.

    Returns
    ---------------------------------
    tuple[str, str, str]
        Title, description and content of the site.
    """
    # Extract title
    title = s.title.text.strip() if s.title is not None else parse_hostname(url)
    title = adjust_text(title)

    # Extract description
    description = s.find('meta', attrs={'name': 'description'})
    if description is None:
        description = ""
    else:
        description = description.get('content')
        if description is None:
            description = ""
        else:
            description = adjust_text(description)

    # Extract contents
    body = s.find('body')
    if body is None:
        content = ""
    else:
        content = adjust_text(body.text)
    # Also, extract the first N words (N: max_content_words)
    words = content.split()
    if len(words) > max_content_length:
        content = " ".join(words[:max_content_length])

    return title, description, content


def extract_links(
    s: BeautifulSoup,
    origin_url: str,
    robots_urls: Optional[tuple[set[str], set[str]]]
) -> Optional[set[str]]:
    """
    Extract onion URLs from the site content.

    Parameters
    -------------------------------
    s: BeautifulSoup
        Used for scraping.
    origin_url: str
        Original URL which is scraped.

    Returns
    -------------------------------
    list[str]
        List of onion URLs.
    """
    urls = set()

    allowed_urls: set[str] = set()
    disallowed_urls: set[str] = set()

    if robots_urls is not None:
        allowed_urls, disallowed_urls = robots_urls

    for link in s.find_all('a'):
        url = link.get('href')
        if url is None or url == '' or url == origin_url or url in disallowed_urls:
            continue
        if is_internal_link(url):
            continue
        if is_url(url) is False:
            url = parse_link_url(origin_url, url)
        if is_http(url) is False:
            continue
        if is_onion_url(url) is False:
            continue
        urls.add(url)

    # Also add allowed urls
    urls |= allowed_urls

    return urls