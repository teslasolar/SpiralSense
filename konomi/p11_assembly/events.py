# SYM-L11 | p=11 | Tension/Release Events
# Locate peaks, drops, and singular moments.

import numpy as np


def extract_events(rms, pitch, centroid, onset_env, duration, min_len, hop, sr):
    """Find tension peaks, release moments, brightness spikes."""
    times = np.arange(min_len) * hop / sr

    top5 = np.argsort(rms)[-5:][::-1]
    tension = [{"time_sec": round(float(times[f]), 1),
                "rms": round(float(rms[f]), 5)} for f in sorted(top5)]

    rms_diff = np.diff(rms)
    drops = np.argsort(rms_diff)[:3]
    releases = [{"time_sec": round(float(times[f]), 1),
                 "drop": round(float(rms_diff[f]), 5)} for f in sorted(drops)]

    top3b = np.argsort(centroid)[-3:][::-1]
    bright = [{"time_sec": round(float(times[f]), 1),
               "centroid_hz": round(float(centroid[f]), 1)} for f in sorted(top3b)]

    segs = 8
    seg_sz = min_len // segs
    density = [round(float(np.mean(onset_env[i*seg_sz:(i+1)*seg_sz])), 4)
               for i in range(segs)]

    return {
        "tension_peaks": tension, "release_moments": releases,
        "brightness_spikes": bright, "onset_density_arc": density,
    }
