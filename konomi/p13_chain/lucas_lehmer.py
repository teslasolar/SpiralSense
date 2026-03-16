# SYM-L13 | p=13 | Lucas-Lehmer Core
# The mathematical heart of the cascade.

import numpy as np


def compute_ll_step(s_prev, modulus):
    """One step: S_k = S_{k-1}^2 - 2 (mod Mp)."""
    return (pow(s_prev, 2, modulus) - 2) % modulus


def derive_s0_seed(pitch_hz, mersenne_prime):
    """Derive S0 seed from pitch. Modulates around canonical 4."""
    if pitch_hz <= 0:
        return 4
    log_p = np.log10(max(pitch_hz, 20))
    norm = (log_p - np.log10(20)) / (np.log10(20000) - np.log10(20))
    seed_range = min(mersenne_prime - 1, 1000)
    seed = int(4 + norm * seed_range) % mersenne_prime
    return max(seed, 2)


def coherence_proximity(cascade_val, mersenne_prime):
    """How close to zero (prime confirmation)? 0.0=far, 1.0=coherent."""
    if mersenne_prime <= 1:
        return 0.0
    dist = min(cascade_val, mersenne_prime - cascade_val)
    return 1.0 - (dist / (mersenne_prime / 2))


def compute_spiral_radius(frame_idx, total_frames, amplitude):
    """Dynamic radius — same as SpiralSense renderer."""
    base = 5.0 + (frame_idx / max(total_frames - 1, 1)) * 95.0
    return base + amplitude * 2.0
