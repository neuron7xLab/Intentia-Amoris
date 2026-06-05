from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from intentia_amoris.config import get_settings
from intentia_amoris.memory.models import Base


def make_engine(url: str | None = None) -> AsyncEngine:
    settings = get_settings()
    db_url = url or settings.active_database_url
    return create_async_engine(db_url, echo=False, pool_pre_ping=True)


engine = make_engine()
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
