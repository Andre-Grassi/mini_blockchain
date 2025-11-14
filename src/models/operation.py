"""Operation enumeration for blockchain transactions.

Defines the types of operations clients can perform: DEPOSIT (add minicoins),
WITHDRAW (remove minicoins), NAME (register client identity), and QUIT
(close connection). Used for message parsing and transaction validation.

Authors: Andre Grassi de Jesus, Ricardo Faria
Last Modified: Nov. 14 2025
"""

from enum import Enum


class Operation(Enum):
    """Defines the types of operations that can be performed by the client."""

    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    QUIT = "q"
    NAME = "name"  # Operation that informs the server of the client's name
