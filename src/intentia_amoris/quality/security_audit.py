from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

import typer

CRITICAL_FILES = [
    "src/intentia_amoris/security/auth.py",
    "src/intentia_amoris/security/audit.py",
    "src/intentia_amoris/security/validation.py",
    "src/intentia_amoris/policies/consent.py",
    "src/intentia_amoris/api.py",
    "contracts/security/ZERO_TRUST_CONTROL_MAP.json",
]


@dataclass(frozen=True, slots=True)
class AuditCheck:
    key: str
    ok: bool
    detail: str


def run_security_audit(root: Path = Path(".")) -> dict:
    checks: list[AuditCheck] = []

    for rel in CRITICAL_FILES:
        checks.append(
            AuditCheck(
                key=f"file_exists:{rel}",
                ok=(root / rel).exists(),
                detail=rel,
            )
        )

    env_example = (root / ".env.example").read_text(encoding="utf-8") if (root / ".env.example").exists() else ""
    checks.append(
        AuditCheck(
            key="env_requires_api_auth",
            ok="INTENTIA_REQUIRE_API_AUTH=true" in env_example,
            detail="fail-closed API auth default",
        )
    )
    checks.append(
        AuditCheck(
            key="env_has_secret_key_placeholder",
            ok="INTENTIA_SECRET_KEY=" in env_example,
            detail="runtime secret configured via environment",
        )
    )

    api_text = (root / "src/intentia_amoris/api.py").read_text(encoding="utf-8")
    checks.append(
        AuditCheck(
            key="api_has_rate_limit_dependency",
            ok="rate_limit_dependency" in api_text,
            detail="rate limiting wired into protected endpoints",
        )
    )
    checks.append(
        AuditCheck(
            key="api_has_api_key_dependency",
            ok="require_api_key" in api_text,
            detail="API key dependency wired into protected endpoints",
        )
    )
    checks.append(
        AuditCheck(
            key="media_consent_before_store",
            ok=api_text.find("ConsentGate().evaluate_event") < api_text.find("data = await file.read()"),
            detail="media upload blocks before reading/persistence when consent missing",
        )
    )

    failed = [asdict(c) for c in checks if not c.ok]
    return {
        "ok": not failed,
        "checks": [asdict(c) for c in checks],
        "failed": failed,
        "score": round(sum(1 for c in checks if c.ok) / max(1, len(checks)), 3),
    }


def main() -> None:
    report = run_security_audit(Path("."))
    typer.echo(json.dumps(report, indent=2, ensure_ascii=False))
    if not report["ok"]:
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
