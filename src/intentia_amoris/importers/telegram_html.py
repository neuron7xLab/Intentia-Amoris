from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import hashlib
import json
import re
import zipfile

from bs4 import BeautifulSoup


@dataclass(frozen=True, slots=True)
class TelegramMedia:
    kind: str
    href: str
    sha256: str | None = None
    size: int | None = None


@dataclass(frozen=True, slots=True)
class TelegramMessage:
    message_id: str
    timestamp_raw: str | None
    day: str | None
    sender_raw: str | None
    actor: str
    text: str
    media: list[TelegramMedia]
    reactions: list[str]
    reply_to: str | None
    links: list[str]

    def to_json(self) -> dict[str, Any]:
        data = asdict(self)
        data["media"] = [asdict(m) for m in self.media]
        return data


def normalize_actor(sender: str | None) -> str:
    value = (sender or "").strip()
    if value == "Yaroslav":
        return "self"
    if "Дарія" in value or "Даша" in value or "ДВ" in value:
        return "partner"
    return "unknown"


def _text(node) -> str:
    return node.get_text("\n", strip=True) if node else ""


def parse_telegram_html(path: str | Path) -> list[TelegramMessage]:
    """
    Parse Telegram Desktop HTML export into immutable event-like records.

    The parser intentionally preserves raw sender names, emoji reactions, replies,
    links, and media references. It does not infer emotions or intentions.
    """
    path = Path(path)
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    messages: list[TelegramMessage] = []
    current_sender: str | None = None
    current_day: str | None = None

    for div in soup.select("div.message"):
        classes = div.get("class", [])
        message_id = div.get("id", "")

        if "service" in classes:
            details = div.select_one(".body.details")
            if details:
                current_day = details.get_text(" ", strip=True)
            continue

        date_el = div.select_one(".date.details")
        timestamp_raw = date_el.get("title") if date_el else None

        from_el = div.select_one(".from_name")
        sender_raw = from_el.get_text(" ", strip=True) if from_el else current_sender
        if sender_raw:
            current_sender = sender_raw

        text_el = div.select_one(".text")
        body_text = _text(text_el)

        media: list[TelegramMedia] = []
        for anchor in div.select("a[href]"):
            classes_str = " ".join(anchor.get("class", []))
            href = anchor.get("href")
            if not href:
                continue

            if "photo_wrap" in classes_str:
                kind = "photo"
            elif "video_file_wrap" in classes_str:
                kind = "video"
            elif "media_voice_message" in classes_str:
                kind = "voice"
            elif "media_audio_file" in classes_str:
                kind = "audio"
            elif "media_file" in classes_str:
                kind = "file"
            else:
                continue

            media.append(TelegramMedia(kind=kind, href=href))

        call = div.select_one(".media_call")
        if call:
            title = _text(call.select_one(".title"))
            status = _text(call.select_one(".status"))
            media.append(TelegramMedia(kind="call", href=f"call:{title}:{status}"))

        reactions = [
            emoji.get_text("", strip=True)
            for emoji in div.select(".reaction .emoji")
            if emoji.get_text("", strip=True)
        ]

        reply_anchor = div.select_one(".reply_to a")
        reply_to = reply_anchor.get("href") if reply_anchor else None

        links: list[str] = []
        if text_el:
            links = [a.get("href") for a in text_el.select("a[href]") if a.get("href")]

        messages.append(
            TelegramMessage(
                message_id=message_id,
                timestamp_raw=timestamp_raw,
                day=current_day,
                sender_raw=sender_raw,
                actor=normalize_actor(sender_raw),
                text=body_text,
                media=media,
                reactions=reactions,
                reply_to=reply_to,
                links=links,
            )
        )

    return messages


def attach_media_hashes(
    messages: list[TelegramMessage],
    archive_path: str | Path,
) -> list[TelegramMessage]:
    """
    Adds sha256 and byte size for media entries present inside the Telegram export zip.
    The raw media is not interpreted here. Vision/audio models can attach descriptions later.
    """
    archive_path = Path(archive_path)
    with zipfile.ZipFile(archive_path) as zf:
        names = set(zf.namelist())
        out: list[TelegramMessage] = []
        for message in messages:
            media_out: list[TelegramMedia] = []
            for item in message.media:
                if item.href.startswith("call:") or item.href not in names:
                    media_out.append(item)
                    continue
                payload = zf.read(item.href)
                media_out.append(
                    TelegramMedia(
                        kind=item.kind,
                        href=item.href,
                        sha256=hashlib.sha256(payload).hexdigest(),
                        size=len(payload),
                    )
                )
            out.append(
                TelegramMessage(
                    message_id=message.message_id,
                    timestamp_raw=message.timestamp_raw,
                    day=message.day,
                    sender_raw=message.sender_raw,
                    actor=message.actor,
                    text=message.text,
                    media=media_out,
                    reactions=message.reactions,
                    reply_to=message.reply_to,
                    links=message.links,
                )
            )
    return out


def write_jsonl(messages: list[TelegramMessage], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for message in messages:
            f.write(json.dumps(message.to_json(), ensure_ascii=False) + "\n")


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def summarize_messages(messages: list[TelegramMessage]) -> dict[str, Any]:
    from collections import Counter

    sender_counts = Counter(m.sender_raw or "unknown" for m in messages)
    actor_counts = Counter(m.actor for m in messages)
    media_counts = Counter(media.kind for m in messages for media in m.media)
    reaction_counts = Counter(reaction for m in messages for reaction in m.reactions)
    text_messages = sum(1 for m in messages if m.text.strip())
    media_messages = sum(1 for m in messages if m.media)
    reply_messages = sum(1 for m in messages if m.reply_to)
    link_messages = sum(1 for m in messages if m.links)

    return {
        "message_count": len(messages),
        "text_message_count": text_messages,
        "media_message_count": media_messages,
        "reply_message_count": reply_messages,
        "link_message_count": link_messages,
        "sender_counts": dict(sender_counts),
        "actor_counts": dict(actor_counts),
        "media_counts": dict(media_counts),
        "reaction_counts": dict(reaction_counts),
        "first_timestamp": messages[0].timestamp_raw if messages else None,
        "last_timestamp": messages[-1].timestamp_raw if messages else None,
        "days": sorted({m.day for m in messages if m.day}),
    }


def extract_dialogue_signals(messages: list[TelegramMessage]) -> dict[str, Any]:
    """
    Deterministic, audit-friendly signal extraction.

    These are not diagnoses and not claims about inner states.
    They are observable linguistic/behavioral traces for later review.
    """
    lexical_sets = {
        "care": ("добро", "спалось", "напиши", "пожалуйста", "умничка", "дякую", "спок", "киць"),
        "desire": ("хочу", "тело", "тіло", "трогать", "ласкав", "поціл", "кайф", "член", "секс"),
        "boundary": ("не хочу", "не планирую", "згода", "согласна", "не дав", "не на лавочках"),
        "future_story": ("істор", "наратив", "назавжди", "майбут", "маніфест", "краще"),
        "uncertainty": ("не знаю", "можливо", "що робити", "ахуї", "треш"),
        "repair_iteration": ("ітерац", "дай мені час", "можу краще", "зробив", "чекай"),
    }
    counts = {k: 0 for k in lexical_sets}
    examples: dict[str, list[dict[str, str | None]]] = {k: [] for k in lexical_sets}

    for m in messages:
        text = m.text.lower()
        for key, terms in lexical_sets.items():
            if any(term in text for term in terms):
                counts[key] += 1
                if len(examples[key]) < 8:
                    examples[key].append(
                        {
                            "id": m.message_id,
                            "timestamp": m.timestamp_raw,
                            "actor": m.actor,
                            "text": m.text[:240],
                        }
                    )

    return {
        "signal_counts": counts,
        "examples": examples,
        "interpretation_rule": (
            "Counts are observable text signals only. They must not be treated as proof "
            "of hidden feelings, hormones, consent, or pathology."
        ),
    }


def build_media_manifest(messages: list[TelegramMessage]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for m in messages:
        for media in m.media:
            out.append(
                {
                    "message_id": m.message_id,
                    "timestamp": m.timestamp_raw,
                    "actor": m.actor,
                    "sender_raw": m.sender_raw,
                    "kind": media.kind,
                    "href": media.href,
                    "sha256": media.sha256,
                    "size": media.size,
                }
            )
    return out
