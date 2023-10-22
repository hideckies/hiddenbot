import httpx
from rich.console import Console
import typer
from typing import Optional
from typing_extensions import Annotated

from .config import get_proxy, check_onion_url, check_tor
from .__version__ import __version__

app = typer.Typer(pretty_exceptions_enable=False)

console = Console()


@app.callback()
def callback() -> None:
    """
    Dark Web Crawler
    """


@app.command(name="run", help="Run HiddenBot.", rich_help_panel="Crawl Commands")
def run(
    url: Annotated[
        str, typer.Option(
            "--url", "-u",
            help="A URL of an onion service to crawl.",
            rich_help_panel="Run Options")
    ],
    proxy: Annotated[
        Optional[str], typer.Option(
            "--proxy", "-x",
            help="A SOCKS5 proxy address e.g. 10.0.0.1:1234",
            rich_help_panel="Run Options")
    ] = "127.0.0.1:9050",
    depth: Annotated[
        Optional[int], typer.Option(
            "--depth", "-d",
            help="Depth to follow links.",
            rich_help_panel="Run Options")
    ] = 2
) -> None:
    if check_onion_url(url) is False:
        console.print("Specified URL is not for onion service.", style="red")
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


@app.command(name="version", help="Display the version of HiddenBot", rich_help_panel="General Commands")
def version() -> None:
    console.print(f"HiddenBot version {__version__}")