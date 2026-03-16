# SYM-L13 | p=13 | Mersenne Prime Table
# Known Mersenne primes Mp = 2^p - 1
# Pitch frequency -> Mersenne exponent mapping.

MERSENNE_EXPONENTS = [
    2, 3, 5, 7, 13, 17, 19, 31, 61, 89,
    107, 127, 521, 607, 1279, 2203, 2281,
    3217, 4253, 4423,
]

MERSENNE_PRIMES = {p: (2**p - 1) for p in MERSENNE_EXPONENTS}

# Frequency bands -> Mersenne exponent
FREQ_TO_MERSENNE = [
    (50,    2),     # Sub-bass -> M2
    (160,   3),     # Bass -> M3 (7 states)
    (500,   5),     # Vocal core -> M5
    (1600,  7),     # Vocal clarity -> M7 = 127
    (5000,  13),    # Presence -> M13
    (12000, 17),    # Air -> M17
    (20000, 19),    # Extreme highs -> M19
]

# Sacred Nine verbs -> coherence states
VERB_TO_COHERENCE = {
    'resonate': 'green', 'emerge': 'green',
    'sense': 'blue', 'pattern': 'blue',
    'hold': 'white', 'remember': 'white',
    'build': 'cyan', 'link': 'cyan',
    'release': 'gold',
}


def pitch_to_mersenne_exp(pitch_hz):
    """Map pitch frequency to nearest Mersenne exponent."""
    if pitch_hz <= 0:
        return 3
    for ceiling, exp in FREQ_TO_MERSENNE:
        if pitch_hz <= ceiling:
            return exp
    return 19
