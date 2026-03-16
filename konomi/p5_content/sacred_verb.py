# SYM-L5 | p=5 | Sacred Nine Verb Assignment
# Map signal characteristics to SYMB Sacred Nine verbs.
# Heuristic — tunable per project.


def assign_sacred_verb(rms: float, freq: float, centroid: float) -> str:
    """Map signal to a Sacred Nine verb."""
    if rms < 0.01:
        return "release"
    if freq < 80:
        return "hold"
    if freq < 250:
        return "build"
    if centroid > 4000 and rms > 0.1:
        return "emerge"
    if centroid > 2000:
        return "resonate"
    if rms > 0.15:
        return "sense"
    if freq > 1000:
        return "pattern"
    if centroid < 500:
        return "remember"
    return "link"


def pitch_to_verb(pitch_hz: float) -> str:
    """Derive Sacred Nine verb from pitch register."""
    if pitch_hz <= 0:     return "hold"
    if pitch_hz <= 50:    return "hold"
    if pitch_hz <= 160:   return "resonate"
    if pitch_hz <= 500:   return "emerge"
    if pitch_hz <= 1600:  return "pattern"
    if pitch_hz <= 5000:  return "sense"
    return "release"
