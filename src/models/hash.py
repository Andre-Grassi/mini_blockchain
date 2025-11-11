#
# Authors: Andre Grassi de Jesus, Ricardo Faria
#

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from models.block import Block

# Imports Server only during static type checking (not at runtime) to avoid
# circular dependency.
if TYPE_CHECKING:
    from models.server import Server


class Hash:
    @staticmethod
    def compute_hash(server: Server, block: Block, previous_block: Block) -> bytes:
        """Calculates the hash for the block using SHA256"""
        payload = block.serialize()

        hash_obj = hashlib.sha256()

        # If it's not the genesis, use last hash
        if previous_block is not None:
            last_hash = previous_block.hash_b
            hash_obj.update(last_hash)

        hash_obj.update(payload)

        return hash_obj.digest()

    @staticmethod
    def validate_block_hash(
        server: Server, block: Block, previous_block: Block
    ) -> bool:
        # Validate current block's hash
        is_hash_valid = block.hash_b == Hash.compute_hash(server, block, previous_block)
        return is_hash_valid

    @staticmethod
    def validate_blockchain_hash(server: Server):
        if len(server.block_chain) > 0:
            # Validate genesis block
            is_genesis_valid = Hash.validate_block_hash(
                server, server.block_chain[0], None
            )

            if not is_genesis_valid:
                return False

            # Validate all blocks
            for index in range(1, len(server.block_chain)):
                curr_block = server.block_chain[index]
                prev_block = server.block_chain[index - 1]
                if not Hash.validate_block_hash(server, curr_block, prev_block):
                    return False

        return True
