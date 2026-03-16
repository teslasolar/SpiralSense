# SYM-L7 | p=7 | Audio Analysis
# Prepare metadata for visualization.

import numpy as np
from konomi.p2_identity.constants import FREQ_BANDS
from .color_map import map_pitch_to_color


def analyze_audio(amplitude, pitch, frame_rate):
    """Compute visualization metadata from audio arrays."""
    n = len(amplitude)
    duration = n / frame_rate
    valid_pitch = pitch[pitch > 0]

    seg_size = max(1, n // 10)
    markers = []
    for i in range(10):
        s, e = i * seg_size, min((i + 1) * seg_size, n)
        sa, sp = amplitude[s:e], pitch[s:e]
        vp = sp[sp > 0]
        avg_p = float(np.mean(vp)) if len(vp) > 0 else 0
        markers.append({
            'time_start': s / frame_rate, 'time_end': e / frame_rate,
            'avg_amp': float(np.mean(sa)), 'avg_pitch': avg_p,
            'color': map_pitch_to_color(avg_p),
        })

    sil_thr = np.mean(amplitude) * 0.05
    sil_pct = float(np.sum(amplitude < sil_thr) / n * 100)
    mt = float(np.argmax(np.abs(np.diff(amplitude))) / frame_rate)

    singular = []
    if len(valid_pitch) > 0:
        thr = np.percentile(valid_pitch, 95)
        last = -999
        for idx in np.where(pitch > thr)[0]:
            t = idx / frame_rate
            if t - last > 5.0:
                singular.append(round(t, 1))
                last = t
        singular = singular[:8]

    cc = {c: 0 for c, _, _, _, _ in FREQ_BANDS}
    for p in pitch:
        c = map_pitch_to_color(p)
        if c in cc: cc[c] += 1
    total = max(sum(cc.values()), 1)
    cd = {c: round(v / total * 100, 1) for c, v in cc.items()}

    return {
        'duration': duration, 'frames': n, 'frame_rate': frame_rate,
        'amplitude_min': float(np.min(amplitude)),
        'amplitude_max': float(np.max(amplitude)),
        'amplitude_mean': float(np.mean(amplitude)),
        'pitch_min': float(np.min(valid_pitch)) if len(valid_pitch) else 0,
        'pitch_max': float(np.max(valid_pitch)) if len(valid_pitch) else 0,
        'pitch_mean': float(np.mean(valid_pitch)) if len(valid_pitch) else 0,
        'temporal_markers': markers, 'silence_pct': sil_pct,
        'max_tension_time': mt, 'singular_times': singular,
        'color_dist': cd,
    }
