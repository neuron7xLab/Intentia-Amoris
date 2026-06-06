from __future__ import annotations

from typing import Callable

GATES = tuple(f"G{i}" for i in range(1, 12))


def run_gates(checks: dict[str, Callable[[], bool]]) -> tuple[bool, tuple[tuple[str, bool], ...]]:
    rows: list[tuple[str, bool]] = []
    for gate in GATES:
        ok = bool(checks.get(gate, lambda: False)())
        rows.append((gate, ok))
        if not ok:
            return