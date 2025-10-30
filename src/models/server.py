import socket
from typing import Optional
from network_node import NetworkNode
from block import Block
from models.acc_creation_block import AccCreationBlock


class Server(NetworkNode):
    def __init__(self, port: int):
        super().__init__()

        self.ip = self._get_own_ip()
        self.port = port
        self.block_chain = []

    def bind_socket(self):
        self.socket.bind((self.ip, self.port))

    def compute_hash(self, block: Block, last_hash: str) -> str:
        return "hash placeholder"

    def compute_genesis_hash(self, block: Block):
        if self.block_chain.count > 0 and block != self.block_chain[0]:
            raise RuntimeError(
                "Cannot compute hash of a block without last hash, since genesis has already been calculated"
            )

    def _get_own_ip(self) -> str:
        aux_socket = None
        try:
            # Create a UDP socket
            aux_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Connect to an extern IP
            # 8.8.8.8 IP is a public DNS from Google
            aux_socket.connect(("8.8.8.8", 1))

            # Get local IP associated with this socket
            own_ip = aux_socket.getsockname()[0]
        except Exception as e:
            print(f"Couldn't get local IP: {e}")
        finally:
            if aux_socket:
                aux_socket.close()

        return own_ip
