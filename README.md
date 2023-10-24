# HiddenBot

Dark web crawler.

## Prerequisites

### Tor

Access to onion services, we need to use **Tor** proxy.

```sh
# If tor is not installed...
sudo apt install tor

tor &
```

To check if you're using Tor from command line, run the following command:

```sh
curl -fsSL -x socks5://127.0.0.1:9050 check.torproject.org | grep Congratulations
```

If the content "Congratulations. This browser is configured to use Tor." appeared, your Tor proxy configuration is correct.

### Virual Machine (Optional)

It's recommended to use a virtual machine for more securely connecting to dark web.

<br />

## Usage

```sh
hiddenbot run -u https://xxx...xxx.onion/

# Depth (-d)
hiddenbot run -u https://xxx...xxx.onion/ -d 5

# Output (-o)
hiddenbot run -u https://xxx...xxx.onion/ -o result.json
```

- `hiddenbot` currently extracts **title**, **description** and **URL** only.
- Extracted data is saved to a **JSON** file.

<br />

## Installation

### From Pip

```sh
pip install hiddenbot
```

### From Source

```sh
git clone https://github.com/hideckies/hiddenbot.git
cd hiddenbot
poetry install
poetry shell
hiddenbot --help
```