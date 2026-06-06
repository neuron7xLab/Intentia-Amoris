from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable

GATES = tuple(f"G{i}" for i in range(1, 12))


@dataclass(frozen=True, slots=True)
class GateResult:
    gate: str
    ok: bool
    ms: float
    note: str = ""


@dataclass(frozen=True, slots=True)
class GateReport:
   