# SYM-L7 | p=7 | Spiral Geometry
# Build spiral coordinates. All views share the same geometry.

import numpy as np


def build_spiral_geometry(amplitude, pitch, meta):
    """Build spiral geometry. Dynamic scaling — canvas always fits."""
    n = len(amplitude)
    duration = meta['duration']
    pitch_max = meta['pitch_max'] if meta['pitch_max'] > 0 else 1000

    r_min, r_max = 5.0, 100.0
    t = np.linspace(0, duration, n)
    radius = r_min + (t / duration) * (r_max - r_min)
    radius += amplitude * (r_max * 0.02)

    rotations = float(np.clip((duration / 60.0) * 2.0, 4.0, 48.0))
    theta = np.linspace(0, rotations * 2 * np.pi, n)

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = (pitch / (pitch_max + 1e-10)) * 55

    return x, y, z, theta, radius
