# SYM-L2 | p=2 | SYMB Constants
# The kernel values that define the system.
# Remove any one and the product changes.

SYMB_VERSION = "1.2.0"

# Konomi constant: kappa = 1/phi (golden ratio inverse)
KONOMI_CONSTANT = 1.0 / ((1 + 5 ** 0.5) / 2)  # ~0.6180339887

# Sacred Nine verbs — the grammar of signal
SACRED_NINE = [
    "sense", "build", "link", "hold",
    "release", "pattern", "resonate",
    "emerge", "remember",
]

# Frequency bands — pitch as light
FREQ_BANDS = [
    ('#FF0000', '20-50Hz',    'Sub-bass',            0.00, 0.10),
    ('#FF8000', '50-160Hz',   'Bass / Body',         0.10, 0.25),
    ('#FFFF00', '160-500Hz',  'Vocal Core / Warmth', 0.25, 0.40),
    ('#00FF00', '500-1.6kHz', 'Vocal Clarity',       0.40, 0.55),
    ('#0000FF', '1.6-5kHz',   'Presence / Harmonics',0.55, 0.70),
    ('#4B0082', '5-12kHz',    'Air / Sparkle',       0.70, 0.85),
    ('#8B00FF', '12-20kHz',   'Extreme Highs',       0.85, 1.00),
]

# Vocal register boundaries (Hz)
REGISTER_MAP = [
    (0,    85,   "bass"),
    (85,   120,  "baritone"),
    (120,  180,  "tenor"),
    (180,  260,  "alto"),
    (260,  350,  "mezzo_soprano"),
    (350,  9999, "soprano_or_falsetto"),
]

NOTES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
