import json
from rich.console import Console


class OnionSite:
    """
    An onion site information which is crawled.
    """
    def __init__(self, title: str, description: str, url: str) -> None:
        self.title = title
        self.description = description
        self.url = url


    def print_info(self, console: Console):
        """
        Print information of an onion site.

        Parameterss
        ------------------------------
        console: Console
            Console instance for outputs.
        """
        console.print()
        console.print(":party_popper: Onion Site Found!")
        console.print(f"Title: {self.title}")
        console.print(f"Description: {self.description}")
        console.print(f"URL: {self.url}")
        console.print()


    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)