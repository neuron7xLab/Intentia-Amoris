from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetrievalReport:
    schema_version: str
    subject: str
    selected_count: int
    omitted_count: int
    ok: bool
