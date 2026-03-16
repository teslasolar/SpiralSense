# SYM-L17 | p=17 | Health Metrics
# The observer watches the system from within.

import konomi


def check_health():
    """Report system health metrics."""
    return {
        "fold": konomi.FOLD,
        "primes": konomi.PRIMES,
        "version": konomi.VERSION,
        "layers": {
            2:  _check("konomi.p2_identity"),
            3:  _check("konomi.p3_storage"),
            5:  _check("konomi.p5_content"),
            7:  _check("konomi.p7_connection"),
            11: _check("konomi.p11_assembly"),
            13: _check("konomi.p13_chain"),
            17: _check("konomi.p17_observer"),
        },
    }


def _check(module_path):
    """Check if a layer module is importable."""
    try:
        __import__(module_path)
        return "green"
    except Exception:
        return "red"
