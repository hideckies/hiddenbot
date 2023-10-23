from bs4 import BeautifulSoup
from typing import Optional
from .utils import adjust_text, parse_hostname, parse_link_url, is_onion_url, is_url


def extract_site_info(s: BeautifulSoup, url: str) -> Optional[tuple[str, str]]:
    """
    Extract the site title, description

    Parameters
    ---------------------------------
    s: BeautifulSoup
        Used for scraping.
    url: str
        URL which is scraped.

    Returns
    ---------------------------------
    tuple[str, str]
        Title and description of the site.
    """
    title = s.title.text.strip() if s.title is not None else parse_hostname(url)
    title = adjust_text(title)

    description = s.find('meta', attrs={'name': 'description'})
    if description is None:
        description = ""
    else:
        description = description.get('content')
        description = adjust_text(description)

    return title, description


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

    allowed_urls = set()
    disallowed_urls = set()

    if robots_urls is not None:
        allowed_urls, disallowed_urls = robots_urls

    for link in s.find_all('a'):
        url = link.get('href')
        if url is None or url == origin_url or url in disallowed_urls:
            continue
        if is_url(url) is False:
            url = parse_link_url(origin_url, url)
        if is_onion_url(url) is False:
            continue
        urls.add(url)

    # Also add allowed urls
    urls |= allowed_urls

    return urls