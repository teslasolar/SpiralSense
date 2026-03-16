# SYM-L11 | p=11 | Signal Classifiers
# Register, texture, resonance — all pattern-derived.

from konomi.p2_identity.constants import REGISTER_MAP


def classify_register(median_hz):
    """Classify vocal register from median pitch."""
    for lo, hi, label in REGISTER_MAP:
        if lo <= median_hz < hi:
            return label
    return "unknown"


def classify_texture(hp_ratio, zcr, centroid):
    """Read surface texture from signal patterns."""
    if hp_ratio > 3.0:     hc = "strongly_harmonic"
    elif hp_ratio > 1.5:   hc = "harmonic_dominant"
    elif hp_ratio > 0.8:   hc = "balanced"
    else:                   hc = "percussive_dominant"

    if zcr > 0.15:         surf = "rough_noisy"
    elif zcr > 0.08:       surf = "textured"
    elif zcr > 0.04:       surf = "smooth"
    else:                   surf = "very_smooth_tonal"

    if centroid > 5000:     bright = "very_bright"
    elif centroid > 3000:   bright = "bright"
    elif centroid > 1500:   bright = "warm_mid"
    else:                   bright = "dark_low"

    return {"harmonic_character": hc, "surface": surf, "brightness": bright}


def resonance_character(hp_ratio, arc):
    if hp_ratio > 2.5 and arc == "CLIMAX_END": return "harmonic_surge"
    if hp_ratio > 2.5: return "sustained_harmonic"
    if arc == "CLIMAX_END": return "building_release"
    return "ambient_resonance"
