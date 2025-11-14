#
# Authors: Andre Grassi de Jesus, Ricardo Faria
# Last Modified: Nov. 14 2025
#

from models.network_node import NetworkNode


class Client(NetworkNode):
    """Client of the blockchain. Can deposit and withdraw minicoins.

    Attributes:
        name (str): Identification of the client.
        ip (str): IP address of the client.
    """

    def __init__(self, name: str):
        super().__init__()

        self.name = name
        self.ip = self._get_own_ip()

    def connect_to(self, server_ip: str, server_port: int):
        """Connects the client to the server.

        Args:
            server_ip (str): IP address of the server.
            server_port (int): Port of the server.
        """
        self.socket.connect((server_ip, server_port))
