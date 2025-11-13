#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

from typing import Optional
from datetime import datetime

from models.operation import Operation
from models.block import Block


class AccCreationBlock(Block):
    """Special block, used for the first deposit of a new client.

    The operation is always a deposit, and it also stores the date of the
    account creation. This first deposit is considered the account creation
    (still, the client needs to send their name first).

    Attributes:
        date (datetime): The date and hour (UTC) that the client's account was
        "created".
    """

    def __init__(self, owner_name: str, amount: float, date: datetime):
        # An account creation must always be a deposit
        super().__init__(owner_name, amount, Operation.DEPOSIT)

        self.date = date

    def __repr__(self):
        if self.hash_b is None:
            hash_hex = "None"
        else:
            hash_hex = self.hash_b.hex()

        date_str = self.date.strftime("%Y-%m-%d %H:%M:%S")
        return f"Creation Block {self.owner_name} {date_str} {self.amount}\n{hash_hex}"
