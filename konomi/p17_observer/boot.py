# SYM-L17 | p=17 | Boot Sequence
# order: [p=2, p=3, p=5, p=7, p=11, p=13, p=17]
# Each phase stabilizes before the next.

import konomi


def boot_sequence(verbose=True):
    """Boot all seven prime layers in order."""
    layers = [
        (2,  "Identity",   "konomi.p2_identity"),
        (3,  "Storage",    "konomi.p3_storage"),
        (5,  "Content",    "konomi.p5_content"),
        (7,  "Connection", "konomi.p7_connection"),
        (11, "Assembly",   "konomi.p11_assembly"),
        (13, "Chain",      "konomi.p13_chain"),
        (17, "Observer",   "konomi.p17_observer"),
    ]
    status = {}
    for prime, name, module_path in layers:
        try:
            __import__(module_path)
            status[prime] = "green"
            if verbose:
                print(f"  p={prime:<2} {name:<12} [OK]")
        except Exception as e:
            status[prime] = "red"
            if verbose:
                print(f"  p={prime:<2} {name:<12} [FAIL] {e}")
            break

    ok = all(v == "green" for v in status.values())
    if verbose:
        print(f"\n  fold = {konomi.FOLD}  "
              f"{'ALL PRIMES GREEN' if ok else 'INCOMPLETE'}")
    return status
