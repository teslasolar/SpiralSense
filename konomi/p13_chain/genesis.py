# SYM-L13 | p=13 | Genesis Block Factory
# Encodes the Konomi Symbeyond Standard as block 0.
# This is the immutable root of every guild chain.

import time
from .guild_block import GuildBlock
from .vector_space import hash_to_vector

GENESIS_PAYLOAD = {
    'standard': 'Konomi Symbeyond Standard v1.0',
    'fold': 510510,
    'primes': [2, 3, 5, 7, 11, 13, 17],
    'layers': {
        '2':  'Identity — you exist because you have a key',
        '3':  'Storage — your data lives on your device',
        '5':  'Content — you sign it, it is yours',
        '7':  'Connection — direct, no intermediary',
        '11': 'Assembly — collective without coordinator',
        '13': 'Chain — permanent record',
        '17': 'Observer — the system watches itself',
    },
    'sacred_nine': [
        'sense', 'build', 'link', 'hold',
        'release', 'pattern', 'resonate',
        'emerge', 'remember',
    ],
    'konomi_constant': 0.6180339887,
    'authors': 'Thomas Frumkin / ERPC + John DuCrest',
    'entity': 'SYMBEYOND AI LLC',
}


def create_genesis():
    """Create and seal the genesis block."""
    block = GuildBlock(
        index=0, timestamp=510510.0,
        layer=13, category='standard',
        label='Genesis — Konomi Symbeyond Standard',
        payload=GENESIS_PAYLOAD,
        prev_hash='0' * 64,
    )
    block.seal()
    block.vector = hash_to_vector(block.block_hash, 13, 0)
    return block
