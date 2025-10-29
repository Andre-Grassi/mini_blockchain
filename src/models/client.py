import socket

BUFFER_SIZE = 1024


class Client:
    def __init__(self, name: str):
        self.name = name
        self.buffer_size = BUFFER_SIZE

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to(self, server_ip: str, server_port: int):
        self.socket.connect((server_ip, server_port))

    def close(self):
        self.socket.close()

    def deposit(self, amount: float):
        return
