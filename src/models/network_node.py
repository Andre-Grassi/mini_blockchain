import socket
from typing import Optional
from operation import Operation

BUFFER_SIZE = 1024


class NetworkNode:
    def __init__(self, buffer_size: Optional[int] = BUFFER_SIZE):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = buffer_size

    def close(self):
        self.socket.close()

    def parse_message(self, message: str):
        parts = message.strip().split()

        # Check if message has incorrect structure
        if len(parts) < 1 or len(parts) > 2:
            return None

        action = parts[0].lower()

        # Check if the action is recognizable
        if action not in ("deposit", "withdraw", "q"):
            return None

        if action == "q":
            return (Operation.QUIT, 0)

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
