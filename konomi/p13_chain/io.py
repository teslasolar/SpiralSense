# SYM-L13 | p=13 | Chain I/O
# Save and load cascade packets.

import json
import os
from dataclasses import asdict


def save_cascade_packet(packet, output_path):
    """Save MersenneCascadePacket to JSON."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(asdict(packet), f, indent=2)
    print(f"[MersenneBridge] Saved -> {output_path}")


def load_cascade_packet(path):
    """Load a saved cascade packet."""
    with open(path) as f:
        return json.load(f)
