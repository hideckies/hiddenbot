import httpx
from rich.console import Console
import typer
from typing import Optional
from typing_extensions import Annotated

from .config import DEFAULT_SOCKS5_HOST, DEFAULT_SOCKS5_PORT, get_proxy, check_tor

app = typer.Typer()

console = Console()


@app.callback()
def callback() -> None:
    """
    Dark Web Crawler
    """


@app.command(name="run", help="Run HiddenBot.", rich_help_panel="Run")
def run(
    proxy: Annotated[
        Optional[str], typer.Option("--proxy", "-x", help="Custom proxy URL e.g. 10.0.0.1:1234")
    ] = "127.0.0.1:9050"
) -> None:
    print(proxy)
    _proxy = get_proxy(proxy)
    if _proxy is None:
        console.print("Please set proxy correctly.", style="red")
        return
    socks5_host, socks5_port = _proxy

    socks5_proxy = f'socks5://{socks5_host}:{socks5_port}'
    print(socks5_proxy)
    with httpx.Client(timeout=60, proxies=socks5_proxy) as client:
        check_tor(client)