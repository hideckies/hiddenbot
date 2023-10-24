from bs4 import BeautifulSoup
import httpx
from rich.console import Console
from rich.prompt import Confirm
import time
import sys
from typing import Optional

from ..save import save_onions
from .result import OnionSite
from .extractor import extract_links, extract_site_info
from .utils import get_robots_urls, parse_hostname


ALLOWED_RESPONSE_STATUS_CODE = [200, 301, 302]


class Crawler:
    """
    Crawler class
    """

    def __init__(
        self,
        console: Console,
        client: httpx.Client,
        url: str,
        depth: int,
        max_content_length: int,
        output: str,
    ) -> None:
        self.console = console

        self.client = client
        self.url = url
        self.depth = depth
        self.max_content_length = max_content_length

        self.output = output

        self.onions: list[OnionSite] = []


    def run(self) -> list[OnionSite]:
        """
        The main function to crawl.
        """
        self.console.print(f"Start crawling from {self.url}.")

        # Initial onion URL
        onion_urls = set([self.url])

        # Crawl each URL
        try:
            for i in range(self.depth):
                self.console.print(f"\nCrawl ID: {i+1}\n")
                if len(onion_urls) == 0:
                    self.console.print("There are no more URLs to crawl.")
                    break
                onion_urls = self.crawl(onion_urls)
        except KeyboardInterrupt as e:
            stop = Confirm.ask("Stop crawling?")
            if stop:
                save_onions(console=self.console, data=self.onions, output=self.output)
                sys.exit(0)
            pass

        return self.onions


    def crawl(self, urls: set[str]) -> set[str]:
        """
        Crawl onion URLs.

        Parameters
        ---------------------------------------
        urls: set[str]
            List of onion URLs.

        Returns
        ---------------------------------------
        set[str]
            List of newly found onion URLs.
        """
        onion_urls = set()
        try:
            for url in urls:
                time.sleep(2)
                found_urls = self.scrape(url)
                if found_urls is None or len(found_urls) == 0:
                    continue
                onion_urls.update(found_urls)
        except KeyboardInterrupt as e:
            stop = Confirm.ask("Stop crawling?")
            if stop:
                save_onions(console=self.console, data=self.onions, output=self.output)
                sys.exit(0)
            return onion_urls

        return onion_urls


    def scrape(self, url: str) -> Optional[set[str]]:
        """
        Scrape contents of specified URL.

        Parameters
        ----------------------------------------
        url: str
            URL to be scraped.

        Returns
        ----------------------------------------
        set[str]
            List of onion URLs.
        """
        flag_same_host = False

        # Check if the onion site has been already scraped.
        for o in self.onions:
            if o.url == url:
                return None
            # If the same host exists, add the flag_same_host.
            # # This flag is used for determining if it's required to get robots.txt or not.
            if parse_hostname(o.url) == parse_hostname(url):
                flag_same_host = True
            
        # Get robots.txt URLs.
        robots_urls: Optional[tuple[set[str], set[str]]] = None
        if flag_same_host is False:
            robots_urls = get_robots_urls(self.client, url)

        # Scrape
        try:
            resp = self.client.get(url)
            if resp.status_code not in ALLOWED_RESPONSE_STATUS_CODE:
                return None
        except KeyboardInterrupt as e:
            stop = Confirm.ask("Stop crawling?")
            if stop:
                save_onions(console=self.console, data=self.onions, output=self.output)
                sys.exit(0)
            return None
        except:
            self.console.print(f"could not access to {url}.")
            return None
                
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Extract the site title and description.
        info = extract_site_info(soup, url, self.max_content_length)
        if info is None:
            return None
        title, description, content = info

        onion_site = OnionSite(title, description, content, url)
        onion_site.print_info(self.console)
        self.add_onion(onion_site)

        # Extract onion URLs from the content.
        onion_urls = extract_links(soup, url, robots_urls)   
   
        return onion_urls  
        

    def add_onion(self, onion: OnionSite) -> None:
        """
        Add the new found onion site to the list.

        Parameters
        ------------------------------------
        onion: OnionSite
            An onion site new found.
        """
        # Check if the new onion URL already exists in the list.
        # If exists, the new onion site is rejected.
        for o in self.onions:
            if o.url == onion.url:
                return

        self.onions.append(onion)