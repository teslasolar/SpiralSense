# SYM-L13 | p=13 | Vector Space
# Derives 3D coordinates from content hashes.
# Each block gets a unique position in the guild chain space.

import hashlib
import math

PRIMES = (2, 3, 5, 7, 11, 13, 17)
LAYER_COLORS = {
    2: '#ff4444', 3: '#ff8800', 5: '#ffdd00', 7: '#00cc44',
    11: '#0088ff', 13: '#8844ff', 17: '#ff44cc',
}


def hash_to_vector(block_hash, layer, index):
    """Derive 3D position from a block hash + layer prime.

    X = spiral angle from hash bytes 0-7
    Y = layer height (prime-indexed)
    Z = radial distance from hash bytes 8-15
    """
    h = bytes.fromhex(block_hash)
    angle_raw = int.from_bytes(h[0:4], 'big')
    radius_raw = int.from_bytes(h[4:8], 'big')

    angle = (angle_raw / 0xFFFFFFFF) * math.pi * 2
    radius = 20 + (radius_raw / 0xFFFFFFFF) * 80
    y = PRIMES.index(layer) * 25 if layer in PRIMES else index * 5

    x = math.cos(angle) * radius
    z = math.sin(angle) * radius
    return [round(x, 4), round(y, 4), round(z, 4)]


def payload_hash(payload):
    """SHA-256 of a payload dict."""
    raw = str(sorted(payload.items())).encode()
    return hashlib.sha256(raw).hexdigest()
