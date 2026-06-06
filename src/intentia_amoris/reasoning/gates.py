from __future__ import annotations

from typing import Callable, TypedDict

GATES = tuple(f"G{i}" for i in range(1, 12))


class GateRow(TypedDict):
    gate: str
    ok: bool
    reason: str


class GateReport(TypedDict):
    ok: bool
    total: int
    passed: int
    rows: tuple[GateRow, ...]


def _call(check: Callable[[], bool] | None) -> tuple[bool, str]:
    if