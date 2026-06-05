from __future__ import annotations

from pathlib import Path


def chunk_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    clean = "\n".join(line.rstrip() for line in text.splitlines()).strip()
    if not clean:
        return []

    paragraphs = [p.strip() for p in clean.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_chars:
            current = f"{current}\n\n{para}".strip()
            continue
        if current:
            chunks.append(current)
        if len(para) <= max_chars:
            current = para
        else:
            start = 0
            while start < len(para):
                chunks.append(para[start : start + max_chars])
                start += max_chars - overlap
            current = ""

    if current:
        chunks.append(current)
    return chunks


def iter_seed_files(seed_root: Path) -> list[Path]:
    return sorted(p for p in seed_root.rglob("*.md") if p.is_file())
