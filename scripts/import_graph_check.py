from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path("src/intentia_amoris")
PKG = "intentia_amoris"


def mod_name(path: Path) -> str:
    rel = path.relative_to("src").with_suffix("")
    return ".".join(rel.parts)


def owned(name: str, modules: set[str]) -> str | None:
    if name in modules:
        return name
    while "." in name:
        name = name.rsplit(".", 1)[0]
        if name in modules:
            return name
    return None


def imports(path: Path, modules: set[str]) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))