from typing import Optional
from datetime import datetime
from operation import Operation
from block import Block


class AccCreationBlock(Block):
    def __init__(self, owner_name: str, amount: float, date: datetime):
        # An account creation must always be a deposit
        super().__init__(owner_name, amount, Operation.DEPOSIT)

        self.date = date
