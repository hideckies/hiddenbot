from stem import Signal
from stem.control import Controller


class TorProxy:
    def __init__(self, addr: str, port: int) -> None:
        controller = Controller.from_port(address=addr, port=port)
        controller.authenticate()


    def change_ip(self) -> None:
        """
        Cnange Tor IP address.
        """
        self.controller.signal(Signal.NEWNYM)