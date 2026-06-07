from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path("src/intentia_amoris")


def module_id(path: Path) -> str:
    return ".".join(path.relative_to("src").with_suffix("").parts)


def nearest(name: str, known: set[str]) -> str | None:
    parts = name.split(".")
    for size in range(len(parts), 0, -1):
        item = ".".join(parts[:size])
        if item in known:
            return item
    return None


def direct_names(path