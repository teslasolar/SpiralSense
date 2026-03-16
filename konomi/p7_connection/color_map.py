# SYM-L7 | p=7 | Color Mapping
# Pitch as light. Frequency to color.

import numpy as np
from konomi.p2_identity.constants import FREQ_BANDS


def map_pitch_to_color(pitch):
    """Map pitch frequency to spectrum color."""
    if pitch <= 0:
        return '#FFFFFF'
    log_p = np.log10(max(float(pitch), 20))
    n = float(np.clip(
        (log_p - np.log10(20)) / (np.log10(20000) - np.log10(20)),
        0, 1
    ))
    for color, _, _, lo, hi in FREQ_BANDS:
        if n < hi:
            return color
    return '#8B00FF'
