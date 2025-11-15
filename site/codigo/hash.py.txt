"""Hash utilities for blockchain integrity.

Computes and validates SHA-256 hashes for blocks in the blockchain. Each block's
hash includes the previous block's hash (except genesis).
Provides methods to validate individual blocks and the entire blockchain.
Does not automatically correct invalid hashes - only reports them.

Authors: Andre Grassi de Jesus, Ricardo Faria
Last Modified: Nov. 14 2025
"""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from models.block import Block

# Imports Server only during static type checking (not at runtime) to avoid
# circular dependency.
if TYPE_CHECKING:
    from models.server import Server


class Hash:
    """Handles the hashing of blocks in the blockchain.

    Uses SHA256 to compute and validate hashes of blocks.
    If it detects an invalid hash, only warns about it, does not correct it. The
    server must pop the invalid blocks itself.

    Attributes:
        None
    """

    @staticmethod
    def compute_hash(server: Server, block: Block, previous_block: Block) -> bytes:
        """Calculates the hash for the block using SHA256

        Previous block's hash is included in the computation, except for the
        genesis block, in this case pass None as previous_block.

        Args:
            server (Server): The server with the blockchain
            block (Block): The block to compute the hash for
            previous_block (Block): The previous block in the chain, or None for
            the genesis block.

        Returns:
            bytes: The computed hash of the block.
        """
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
        """Validates the hash of a block.

        Checks if the stored hash in the block matches the computed hash.

        Args:
            server (Server): The server with the blockchain
            block (Block): The block to validate
            previous_block (Block): The previous block in the chain, or None for
            the genesis block.

        Returns:
            bool: True if the hash is valid, False otherwise.
        """
        # Validate current block's hash
        is_hash_valid = block.hash_b == Hash.compute_hash(server, block, previous_block)
        return is_hash_valid

    @staticmethod
    def validate_blockchain_hash(server: Server) -> bool:
        """Validates the entire blockchain's hashes.

        Needs to be called after adding a new block to ensure the integrity
        of the blockchain.

        Args:
            server (Server): The server with the blockchain

        Returns:
            bool: True if the entire blockchain is valid, False otherwise.
        """
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
