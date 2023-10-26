import json
import os
from rich.console import Console

from .crawl.result import OnionSite


def save_onions(console: Console, data: list[OnionSite], output: str) -> None:
    """
    Save crawled data to a file.
    """
    _, ext = os.path.splitext(output)
    if ext == '.json':
        console.print(f"Save to {output}.")
        save_json(data=data, output=output)


def save_json(data: list[OnionSite], output: str) -> None:
    """
    Save to a json file.
    """
    json_objs = [json.loads(d.to_json()) for d in data]

    with open(output, 'w') as f:
        json.dump(json_objs, f, indent=4, ensure_ascii=False)
