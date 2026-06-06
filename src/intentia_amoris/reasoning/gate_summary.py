from __future__ import annotations


def summarize(rows: tuple[tuple[str, bool], ...]) -> dict[str, int | bool]:
    total = len(rows)
    done = sum(1 for _, ok in rows if ok)
    return {"ok": done == total, "total": total, "done": done}
