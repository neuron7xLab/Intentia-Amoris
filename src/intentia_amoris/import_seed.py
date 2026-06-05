from __future__ import annotations

import asyncio
from pathlib import Path

from intentia_amoris.kernel.embeddings import get_embedding_provider
from intentia_amoris.importers.chunking import chunk_text, iter_seed_files
from intentia_amoris.memory.db import SessionLocal, init_db
from intentia_amoris.memory.repository import add_memory_chunk


async def import_seed(seed_root: Path = Path("seeds")) -> int:
    await init_db()
    embedder = get_embedding_provider()
    count = 0
    async with SessionLocal() as session:
        for path in iter_seed_files(seed_root):
            text = path.read_text(encoding="utf-8")
            namespace = path.parent.name
            title = path.stem
            for i, chunk in enumerate(chunk_text(text)):
                embedding = await embedder.embed(chunk)
                await add_memory_chunk(
                    session,
                    namespace=namespace,
                    title=f"{title}#{i+1}",
                    content=chunk,
                    embedding=embedding,
                    metadata={"source_path": str(path)},
                )
                count += 1
        await session.commit()
    return count


def main() -> None:
    count = asyncio.run(import_seed())
    print(f"imported_chunks={count}")


if __name__ == "__main__":
    main()
