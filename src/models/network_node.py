import socket
from typing import Optional

BUFFER_SIZE = 1024


class NetworkNode:
    def __init__(self, buffer_size: Optional[int] = BUFFER_SIZE):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buffer_size = buffer_size

    def close(self):
        self.socket.close()

    def parse_message(self, message: str):
        parts = message.strip().split()
        if len(parts) < 1 or len(parts) > 2:
            return None

        action = parts[0].lower()

        if action not in ("deposit", "withdraw", "q"):
            return None

        if action == "q":
            return (action, 0)

        amount_s = parts[1]

        try:
            amount = float(amount_s)
        except ValueError:
            return None

        return (action, amount)
