from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path

from intentia_amoris.memory.retrieval_contract import RetrievalResult


@dataclass(frozen=True, slots=True)
class RetrievalReport:
    schema_version: str
    subject: str
    selected_count: int
    omitted_count: int
    selected_hashes: tuple[str, ...]
    ok: bool

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii