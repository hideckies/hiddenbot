# HiddenBot: Dark Web Crawler

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

<br />

## Usage

```sh
hiddenbot run
```