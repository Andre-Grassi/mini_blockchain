#
# Authors: Andre Grassi de Jesus, Ricardo Faria
# Last Modified: Nov. 14 2025
#

from enum import Enum


class Operation(Enum):
    """Defines the types of operations that can be performed by the client."""

    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    QUIT = "q"
    NAME = "name"  # Operation that informs the server of the client's name
