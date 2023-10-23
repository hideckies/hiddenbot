from bs4 import BeautifulSoup
import httpx
from typing import Optional
import re

# Default SOCKS5 proxy
DEFAULT_SOCKS5_HOST = '127.0.0.1'
DEFAULT_SOCKS5_PORT = '9050'

# Regular expressions
REGEX_IPV4_ADDRESS = '((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])'


def get_proxy(proxy: str) -> Optional[tuple[str, str]]:
    """
    Get proxy host and port from command-line argument.
    """
    try:
        [socks5_host, socks5_port] = proxy.split(':')
        return socks5_host, socks5_port
    except:
        return None


def check_tor(client: httpx.Client) -> tuple[bool, str]:
    """
    Check if user is using Tor proxy by accessing `check.torproject.org`.

    Parameters
    ---------------------------------------
    client: httpx.Client
        A httpx client to request

    Returns
    ---------------------------------------
    bool
        User client is connecting Tor or not
    str
        Tor Ip address if user is connecting Tor
    """
    url = "https://check.torproject.org/"

    try:
        resp = client.get(url)
    except Exception as e:
        raise Exception(f"Could not access to {url}. Check proxy setting.")

    soup = BeautifulSoup(resp.text, 'html.parser')
    content = soup.find("div", {"class": "content"})
    if not content:
        raise Exception("could not find content.")
    
    h1_tag = content.find('h1')
    if not h1_tag:
        raise Exception("could not find `h1` tag.")

    connected: bool = False
    if "Congratulations" in h1_tag.text:
        connected = True

    # Get Tor IP address
    ip: str = ""
    p_tags = content.find_all('p')
    for p_tag in p_tags:
        if "Your IP address" in p_tag.text:
            re_ipv4 = re.compile(REGEX_IPV4_ADDRESS)
            results = re.search(re_ipv4, p_tag.text)
            if results:
                ip = results.group()

    return connected, ip