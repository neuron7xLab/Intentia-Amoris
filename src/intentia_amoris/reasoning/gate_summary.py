from __future__ import annotations


def summarize(rows: tuple[tuple[str, bool], ...]) -> dict[str, int | bool | float]:
    total = len(rows)
    done = sum(1 for _, ok in rows if ok)
    score = 1.0 if total == 0 else done / total
    return {"ok": done == total, "total": total, "done": done, "score": score}
