import socket
from network_node import NetworkNode

BUFFER_SIZE = 1024


class Client(NetworkNode):
    def __init__(self, name: str):
        super().__init__()

        self.name = name
        self.buffer_size = BUFFER_SIZE

    def connect_to(self, server_ip: str, server_port: int):
        self.socket.connect((server_ip, server_port))

    def deposit(self, amount: float):
        return
