from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = Field("dev", alias="INTENTIA_ENV")
    timezone: str = Field("Europe/Uzhgorod", alias="INTENTIA_TIMEZONE")
    pair_id: str = Field("yaroslav_dasha", alias="INTENTIA_PAIR_ID")

    database_url: str = Field(
        "postgresql+asyncpg://intentia:intentia@localhost:5432/intentia",
        alias="INTENTIA_DATABASE_URL",
    )
    sqlite_fallback: str = Field(
        "sqlite+aiosqlite:///./intentia_amoris.db",
        alias="INTENTIA_SQLITE_FALLBACK",
    )

    telegram_bot_token: SecretStr = Field(SecretStr(""), alias="TELEGRAM_BOT_TOKEN")
    allowed_user_ids: str = Field("", alias="INTENTIA_ALLOWED_USER_IDS")

    api_keys: str = Field("", alias="INTENTIA_API_KEYS")
    require_api_auth: bool = Field(True, alias="INTENTIA_REQUIRE_API_AUTH")
    allow_insecure_dev: bool = Field(False, alias="INTENTIA_ALLOW_INSECURE_DEV")
    secret_key: SecretStr = Field(SecretStr(""), alias="INTENTIA_SECRET_KEY")
    audit_log_path: Path = Field(Path("./data/audit/audit.jsonl"), alias="INTENTIA_AUDIT_LOG_PATH")
    request_rate_limit_per_minute: int = Field(120, alias="INTENTIA_RATE_LIMIT_PER_MINUTE")
    max_content_chars: int = Field(8000, alias="INTENTIA_MAX_CONTENT_CHARS")
    max_metadata_keys: int = Field(64, alias="INTENTIA_MAX_METADATA_KEYS")
    max_media_bytes: int = Field(15 * 1024 * 1024, alias="INTENTIA_MAX_MEDIA_BYTES")
    allowed_media_extensions: str = Field(
        ".jpg,.jpeg,.png,.webp,.mp3,.wav,.ogg,.m4a,.mp4,.mov",
        alias="INTENTIA_ALLOWED_MEDIA_EXTENSIONS",
    )

    embedding_provider: str = Field("local", alias="INTENTIA_EMBEDDING_PROVIDER")
    embedding_dim: int = Field(384, alias="INTENTIA_EMBEDDING_DIM")
    openai_api_key: SecretStr = Field(SecretStr(""), alias="OPENAI_API_KEY")
    openai_embedding_model: str = Field("text-embedding-3-small", alias="OPENAI_EMBEDDING_MODEL")

    media_root: Path = Field(Path("./data/media"), alias="INTENTIA_MEDIA_ROOT")
    require_partner_consent: bool = Field(True, alias="INTENTIA_REQUIRE_PARTNER_CONSENT")
    default_privacy_scope: str = Field("pair_private", alias="INTENTIA_DEFAULT_PRIVACY_SCOPE")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("env")
    @classmethod
    def normalize_env(cls, value: str) -> str:
        normalized = value.lower().strip()
        if normalized not in {"dev", "test", "staging", "prod"}:
            raise ValueError("Intentia_ENV must be one of dev/test/staging/prod")
        return normalized

    @property
    def allowed_ids(self) -> set[int]:
        ids: set[int] = set()
        for item in self.allowed_user_ids.split(","):
            item = item.strip()
            if not item:
                continue
            try:
                ids.add(int(item))
            except ValueError:
                pass
        return ids

    @property
    def active_database_url(self) -> str:
        if self.env == "test":
            return self.sqlite_fallback
        return self.database_url

    @property
    def parsed_api_keys(self) -> set[str]:
        return {k.strip() for k in self.api_keys.split(",") if k.strip()}

    @property
    def parsed_media_extensions(self) -> set[str]:
        return {e.strip().lower() for e in self.allowed_media_extensions.split(",") if e.strip()}

    @property
    def telegram_token(self) -> str:
        return self.telegram_bot_token.get_secret_value()

    @property
    def openai_key(self) -> str:
        return self.openai_api_key.get_secret_value()

    @property
    def secret_key_value(self) -> str:
        return self.secret_key.get_secret_value()

    def assert_runtime_safe(self) -> None:
        """
        Fail-closed runtime check.

        Dev can be intentionally insecure only with Intentia_ALLOW_INSECURE_DEV=true.
        Staging/prod must have API auth, at least one API key and a long secret key.
        """
        if self.env == "test":
            return

        missing: list[str] = []
        if self.require_api_auth and not self.parsed_api_keys:
            missing.append("Intentia_API_KEYS")
        if self.env in {"staging", "prod"}:
            if not self.require_api_auth:
                missing.append("Intentia_REQUIRE_API_AUTH=true")
            if len(self.secret_key_value) < 32:
                missing.append("Intentia_SECRET_KEY length >= 32")
            if not self.parsed_api_keys:
                missing.append("Intentia_API_KEYS")
        if missing and not self.allow_insecure_dev:
            joined = ", ".join(missing)
            raise RuntimeError(
                f"Unsafe Intentia runtime configuration. Missing/invalid: {joined}. "
                "Set explicit secrets or Intentia_ALLOW_INSECURE_DEV=true for local-only experiments."
            )


@lru_cache
def get_settings() -> Settings:
    return Settings()
