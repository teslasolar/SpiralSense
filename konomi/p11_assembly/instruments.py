# SYM-L11 | p=11 | Instrumentation Detection
# Pattern-derived instrument identification.
# No label assigned without evidence.


def detect_instrumentation(hp_ratio, centroid, zcr, onset,
                           median_pitch, valid_pitch, mfcc):
    """Detect instruments from pattern signatures alone."""
    detected = {}

    if hp_ratio > 1.5 and 60 <= median_pitch <= 520:
        conf = min(1.0, (hp_ratio - 1.5) / 3.0 + 0.5)
        detected["male_vocals"] = {
            "confidence": round(conf, 2),
            "evidence": f"H/P {hp_ratio:.2f}, pitch {median_pitch:.1f}Hz"
        }

    if hp_ratio > 1.5 and median_pitch > 180:
        conf = min(1.0, (hp_ratio - 1.5) / 3.0 + 0.4)
        detected["female_vocals"] = {
            "confidence": round(conf, 2),
            "evidence": f"H/P {hp_ratio:.2f}, pitch {median_pitch:.1f}Hz"
        }

    if hp_ratio < 3.0 and onset > 0.9:
        detected["drums"] = {
            "confidence": round(min(1.0, onset / 2.0), 2),
            "evidence": f"Onset {onset:.3f}, H/P {hp_ratio:.2f}"
        }

    if centroid < 2000 and hp_ratio > 1.2 and median_pitch < 120:
        detected["bass_guitar"] = {
            "confidence": round(min(1.0, (2000-centroid)/2000*0.8), 2),
            "evidence": f"Centroid {centroid:.1f}Hz, pitch {median_pitch:.1f}Hz"
        }

    if hp_ratio > 2.0 and 1500 < centroid < 5000:
        detected["guitar"] = {
            "confidence": round(min(1.0, (hp_ratio-2.0)/2.0+0.4), 2),
            "evidence": f"H/P {hp_ratio:.2f}, centroid {centroid:.1f}Hz"
        }

    dominant = max(detected, key=lambda k: detected[k]["confidence"]) if detected else "unknown"

    return {
        "detected": detected, "dominant": dominant,
        "hp_ratio": round(hp_ratio, 3),
        "note": "Pattern-derived. Confidence = signal evidence.",
    }
