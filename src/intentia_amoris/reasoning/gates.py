from __future__ import annotations

from typing import Callable, TypedDict

GATES = tuple(f"G{i}" for i in range(1, 12))


class GateRow(TypedDict):
    gate: str
    ok: bool
    state: str


class GateReport(TypedDict):
    ok: bool
    total: int
    done: int
    rows: tuple[GateRow, ...]


def run_gates(checks: dict[str, Callable[[], bool]]) -> tuple[bool, tuple[tuple[str, bool], ...]]:
    rows = tuple((gate, bool(checks.get(gate, lambda: False)())) for gate in GATES)
    return all(ok for _, ok in rows),