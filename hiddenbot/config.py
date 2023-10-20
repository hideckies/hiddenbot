import httpx
from typing import Optional
from bs4 import BeautifulSoup

DEFAULT_SOCKS5_HOST = '127.0.0.1'
DEFAULT_SOCKS5_PORT = '9050'

def get_proxy(proxy: str) -> Optional[tuple[str, str]]:
    """
    Get proxy host and port from command-line argument.
    """
    try:
        [socks5_host, socks5_port] = proxy.split(':')
        return socks5_host, socks5_port
    except:
        return None


def check_tor(client: httpx.Client) -> None:
    """
    Check if user is using Tor.
    """
    url = "https://check.torproject.org/"
    resp = client.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    content = soup.find("div", {"class": "content"})
    if not content:
        raise Exception("unable to find content.")
    
    print(content)