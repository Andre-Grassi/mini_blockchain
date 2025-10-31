import socket
from typing import Optional
from models.operation import Operation

BUFFER_SIZE = 1024


class NetworkNode:
    """A node, that can be either the server or many clients.

    It's the base class for both the server and the client.

    Attributes:
        socket (socket): The socket, using TCP/IP and Internet.
        buffer_size (int): Default value is 1024.
    """

    def __init__(self, buffer_size: Optional[int] = BUFFER_SIZE):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = buffer_size  # OPTIMIZE useless?

    def send_str(self, message: str):
        self.socket.sendall(message.encode("utf-8"))

    def send_bytes(self, message: bytes):
        self.socket.sendall(message)

    def close(self):
        self.socket.close()

    def parse_message(self, message: str):
        """Retrieves the info from the message.

        Args:
            message (str): The message, that can be:
                1. q: to close communication
                2. name <client_name>: to inform the client's name to server
                3. deposit <amount>: to deposit money
                4. withdraw <amount>: to withdraw money

        Returns:
            (action, data)

        """
        parts = message.strip().split()

        # Check if message has incorrect structure
        if len(parts) < 1 or len(parts) > 2:
            return None

        action = parts[0].lower()

        # Check if the action is recognizable
        # UGLY hardcoded actions strings
        if action not in ("deposit", "withdraw", "name", "q"):
            return None

        if action == Operation.QUIT.value:
            return (Operation.QUIT, 0)

        elif action == Operation.NAME.value:
            name = parts[1]
            return (Operation.NAME, name)

        amount_s = parts[1]

        # Try to convert string amount to float
        try:
            amount = float(amount_s)
        except ValueError:
            return None

        # Return correct operation according to action
        if action == "deposit":
            return (Operation.DEPOSIT, amount)
        elif action == "withdraw":
            return (Operation.WITHDRAW, amount)

        raise RuntimeError("Unknown error while parsing message")
