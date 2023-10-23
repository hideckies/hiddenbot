from bs4 import BeautifulSoup
from typing import Optional
from .utils import adjust_text, get_hostname, is_onion_url, is_url


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
    title = s.title.text.strip() if s.title is not None else get_hostname(url)
    title = adjust_text(title)

    description = s.find('meta', attrs={'name': 'description'})
    if description is None:
        description = ""
    else:
        description = description.get('content')
        description = adjust_text(description)

    return title, description


def extract_onion_urls(s: BeautifulSoup, origin_url: str) -> Optional[set[str]]:
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
    for link in s.find_all('a'):
        url = link.get('href')
        if url is None or url == origin_url or is_url(url) is False or is_onion_url(url) is False:
            continue
        urls.add(url)
    return urls