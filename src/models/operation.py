#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

from enum import Enum


class Operation(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    QUIT = "q"
    NAME = "name"

