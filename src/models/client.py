#
# Autores: Andre Grassi de Jesus, Ricardo Faria
#

import socket
from models.network_node import NetworkNode
from models.operation import Operation

class Client(NetworkNode):
    """Client of the blockchain. Can deposit and withdraw minicoins.
    
        Attributes:
            name (str): Identification of the client.
    """
    def __init__(self, name: str):
        super().__init__()

        self.name = name

    def connect_to(self, server_ip: str, server_port: int):
        self.socket.connect((server_ip, server_port))

    def deposit(self, amount: float):
        return
