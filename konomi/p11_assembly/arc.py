# SYM-L11 | p=11 | Emotional Arc
# Read the arc from energy movement over time.

import numpy as np


def extract_arc(rms, pitch, hop, duration):
    """Read emotional arc from energy thirds."""
    n = len(rms)
    thirds = n // 3
    e1 = float(np.mean(rms[:thirds]))
    e2 = float(np.mean(rms[thirds:2*thirds]))
    e3 = float(np.mean(rms[2*thirds:]))

    if e2 > e1 and e2 > e3:
        shape, meaning = "PEAK_CENTER", "Builds then releases."
    elif e3 > e1 and e3 > e2:
        shape, meaning = "CLIMAX_END", "Climax at the end."
    elif e1 > e2 and e1 > e3:
        shape, meaning = "FRONT_LOADED", "Opens with peak energy."
    else:
        shape, meaning = "SUSTAINED", "Energy held consistently."

    peak_frame = int(np.argmax(rms))
    peak_time = peak_frame * hop / 44100
    tail = rms[int(n * 0.85):]
    slope = float(np.polyfit(np.arange(len(tail)), tail, 1)[0])
    ending = "decay" if slope < -0.00005 else (
             "sustain" if abs(slope) < 0.00005 else "rise")

    p_thirds = []
    for i in range(3):
        seg = pitch[i*thirds:(i+1)*thirds]
        v = seg[seg > 0]
        p_thirds.append(float(np.mean(v)) if len(v) else 0.0)
    pd = "rising" if p_thirds[2] > p_thirds[0] else (
         "falling" if p_thirds[2] < p_thirds[0] else "stable")

    return {
        "shape": shape, "meaning": meaning,
        "energy_thirds": {"first": round(e1,5), "middle": round(e2,5), "last": round(e3,5)},
        "peak_time_sec": round(peak_time, 1), "ending": ending,
        "ending_slope": round(slope, 7),
        "pitch_direction": pd, "pitch_by_third": [round(v,1) for v in p_thirds],
    }
