# SYM-L11 | p=11 | Assembly (The Collective)
# Collective state, rooms, CRDT synchronization.
# Collective without coordinator.
# Lazy imports — librosa is optional at boot time.


def MetadataExtractor(*args, **kwargs):
    from .extractor import MetadataExtractor as _ME
    return _ME(*args, **kwargs)


def CorpusReader(*args, **kwargs):
    from .corpus import CorpusReader as _CR
    return _CR(*args, **kwargs)
