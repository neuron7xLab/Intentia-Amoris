from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import typer


REQUIRED_PATHS = [
    "README.md",
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yml",
    ".github/workflows/ci.yml",
    ".env.example",
    "src/intentia_amoris/api.py",
    "src/intentia_amoris/telegram_bot.py",
    "src/intentia_amoris/kernel/value_core.py",
    "src/intentia_amoris/kernel/principia.py",
    "src/intentia_amoris/kernel/extrapolation.py",
    "src/intentia_amoris/security/auth.py",
    "src/intentia_amoris/security/audit.py",
    "src/intentia_amoris/security/validation.py",
    "contracts/INTENTIA_VALUE_CONTRACT.json",
    "contracts/FORMAL_AXIOMS.json",
    "contracts/security/ZERO_TRUST_CONTROL_MAP_V8.json",
    "docs/FORMAL_SPECIFICATION.md",
    "docs/VALUE_FUNCTION.md",
    "docs/ARCHITECTURE_V8.md",
    "ui/intentia-dashboard.html",
]


@dataclass(frozen=True, slots=True)
class ProductCheck:
    key: str
    ok: bool
    detail: str


def run_product_audit(root: Path = Path(".")) -> dict:
    checks: list[ProductCheck] = []

    for rel in REQUIRED_PATHS:
        checks.append(ProductCheck(key=f"exists:{rel}", ok=(root / rel).exists(), detail=rel))

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").exists() else ""
    for phrase in [
        "Intentia Amoris",
        "consent-first",
        "event-sourced",
        "zero-trust",
        "value function",
        "Yaroslav ↔ Dasha",
    ]:
        checks.append(ProductCheck(key=f"readme:{phrase}", ok=phrase in readme, detail=phrase))

    env = (root / ".env.example").read_text(encoding="utf-8") if (root / ".env.example").exists() else ""
    checks.append(ProductCheck("env:fail_closed_auth", "INTENTIA_REQUIRE_API_AUTH=true" in env, "API auth default true"))
    checks.append(ProductCheck("env:secret_key", "INTENTIA_SECRET_KEY=" in env, "secret key exists"))

    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8") if (root / "pyproject.toml").exists() else ""
    checks.append(ProductCheck("scripts:intentia-api", "intentia-api" in pyproject, "api console script"))
    checks.append(ProductCheck("scripts:intentia-bot", "intentia-bot" in pyproject, "bot console script"))
    checks.append(ProductCheck("scripts:intentia-value", "intentia-value" in pyproject, "value console script"))

    failed = [asdict(c) for c in checks if not c.ok]
    return {
        "ok": not failed,
        "score": round(sum(1 for c in checks if c.ok) / max(1, len(checks)), 4),
        "checks": [asdict(c) for c in checks],
        "failed": failed,
    }


def main() -> None:
    report = run_product_audit(Path("."))
    typer.echo(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["ok"]:
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
