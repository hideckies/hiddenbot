import httpx
from rich.console import Console
import typer
from typing_extensions import Annotated

from .config import get_proxy, check_tor
from .__version__ import __version__
from .crawl.crawler import Crawler
from .crawl.utils import is_url, is_onion_url
from .save import save_onions


app = typer.Typer(pretty_exceptions_enable=False)

console = Console()


@app.callback()
def callback() -> None:
    """
    Dark Web Crawler
    """


@app.command(
    name="run",
    help="Run HiddenBot.",
    rich_help_panel="Crawl Commands")
def run(
    url: Annotated[
        str, typer.Option(
            "--url", "-u",
            help="A URL of an onion service to crawl.",
            rich_help_panel="Run Options")
    ],
    proxy: Annotated[
        str, typer.Option(
            "--proxy", "-x",
            help="A SOCKS5 proxy address e.g. 10.0.0.1:1234.",
            rich_help_panel="Run Options")
    ] = "127.0.0.1:9050",
    depth: Annotated[
        int, typer.Option(
            "--depth", "-d",
            help="Depth to follow links.",
            rich_help_panel="Run Options")
    ] = 2,
    output: Annotated[
        str, typer.Option(
            "--output", "-o",
            help="Output results to specific file.",
            rich_help_panel="Run Options"
        )
    ] = "onions.json",
    quiet: Annotated[
        bool, typer.Option(
            "--quiet", "-q",
            help="The minimum output while running a crawler.",
            rich_help_panel="Run Options"
        )
    ] = False,
    max_content_length: Annotated[
        int, typer.Option(
            "--max-content-length",
            help="Maximum length of content to extract. `-1` is unlimited.",
            rich_help_panel="Run Options"
        )
    ] = 100
) -> None:
    console = Console(quiet=quiet)

    if is_url(url) is False or is_onion_url(url) is False:
        console.print("Specified URL is not valid or not onion site.", style="red")
        return

    _proxy = get_proxy(proxy)
    if _proxy is None:
        console.print("Please set proxy correctly.", style="red")
        return
    socks5_host, socks5_port = _proxy

    socks5_proxy = f'socks5://{socks5_host}:{socks5_port}'
    console.print(f"Proxy: {socks5_proxy}")
    with httpx.Client(timeout=60, proxies=socks5_proxy) as client:
        result = check_tor(client)
        if result is None:
            return

        connected, tor_ip = result
        console.print(f"Tor Connection: {connected}")
        console.print(f"Tor IP: {tor_ip}")

        if connected is False or tor_ip == "":
            console.print(
                "You're not connecting Tor or could not retrieve your Tor IP address.",
                style="red")
            return
        
        # Start crawling target URL
        crawler = Crawler(
            console=console, client=client, url=url, depth=depth,
            max_content_length=max_content_length, output=output)
        onion_sites = crawler.run()

        if len(onion_sites) == 0:
            console.print("There are no onion sites found.")
            return
        
        # Save to a file
        save_onions(console=console, data=onion_sites, output=output)


@app.command(
    name="version",
    help="Display the version of HiddenBot",
    rich_help_panel="General Commands")
def version() -> None:
    print(f"HiddenBot version {__version__}")
