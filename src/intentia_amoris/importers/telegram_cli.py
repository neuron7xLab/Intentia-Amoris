from __future__ import annotations

from pathlib import Path
import json

import typer
from rich import print

from intentia_amoris.importers.telegram_html import (
    attach_media_hashes,
    build_media_manifest,
    extract_dialogue_signals,
    parse_telegram_html,
    summarize_messages,
    write_jsonl,
)

app = typer.Typer(help="Parse Telegram Desktop HTML exports into Intentia event memory.")


@app.command()
def parse(
    html_path: Path = typer.Argument(..., exists=True, readable=True),
    archive_path: Path | None = typer.Option(None, "--archive", "-a", help="Telegram export zip"),
    out_dir: Path = typer.Option(Path("data/derived/telegram"), "--out", "-o"),
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    messages = parse_telegram_html(html_path)
    if archive_path:
        messages = attach_media_hashes(messages, archive_path)

    write_jsonl(messages, out_dir / "messages.jsonl")
    (out_dir / "summary.json").write_text(
        json.dumps(summarize_messages(messages), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "dialogue_signals.json").write_text(
        json.dumps(extract_dialogue_signals(messages), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "media_manifest.json").write_text(
        json.dumps(build_media_manifest(messages), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    summary = summarize_messages(messages)
    print("[bold green]Intentia Telegram import complete[/bold green]")
    print(summary)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
