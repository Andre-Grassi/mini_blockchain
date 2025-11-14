#
# Authors: Andre Grassi de Jesus, Ricardo Faria
# Last Modified: Nov. 14 2025
#


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

    def send_str(self, connection: socket.socket, message: str):
        message += "\n"  # Used as delimiter
        connection.sendall(message.encode("utf-8"))

    def send_bytes(self, connection: socket.socket, message: bytes):
        message += b"\n"  # Used as delimiter
        connection.sendall(message)

    def close(self):
        self.socket.close()

    def terminate(self):
        """Terminates the socket connection gracefully.

        Calls shutdown and close on the socket and handles potential exceptions.
        """
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            self.socket.close()
        except OSError:
            pass

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
            return (None, None)

        action = parts[0].lower()

        # Check if the action is recognizable
        # UGLY hardcoded actions strings
        if action not in ("deposit", "withdraw", "name", "q"):
            return (None, None)

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

    def _get_own_ip(self) -> str:
        """Gets the local IP address of the node.

        Connects to an external IP with UDP to determine the local IP.

        Returns:
            str: The local IP address. If it fails, returns None.
        """
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
