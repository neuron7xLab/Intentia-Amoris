from __future__ import annotations

from collections import Counter
from math import log2


def shannon_bits(text: str) -> float:
    data = text.encode("utf-8")
    if not data:
        return 0.0
    total = len(data)
    counts = Counter(data)
    return -sum((count / total) * log2(count / total) for count in counts.values())


def entropy_delta(previous: str, current: str) -> float:
    return shannon_bits(current) - shannon_bits(previous)
