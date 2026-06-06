from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from time import perf_counter
from typing import Callable, Mapping


class GateId(StrEnum):
    G1_SYNTAX = "G1_SYNTAX"
    G2_TYPES = "G2_TYPES"
    G3_BOUNDS = "G3_BOUNDS"
    G4_CONTEXT = "G4_CONTEXT"
    G5_INVARIANTS = "G5_INVARIANTS"
    G6_EVIDENCE = "G6_EVIDENCE"
    G7_PRIVACY