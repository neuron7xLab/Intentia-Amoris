from __future__ import annotations


def value_of(item: int | None) -> int:
    return 0 if item is None else int(item)


def after(item: int | None) -> int:
    return value_of(item) + 1


def same_seen(*, stored: int | None, seen: int | None) -> bool:
    return value_of(stored) == value_of(seen)


def next_value(*, base: int | None, token: int | None) -> int | None:
    if value_of(base) != value_of(token):
        return None
    return