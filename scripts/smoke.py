import asyncio

from intentia_amoris.domain import ActorRole, Event, EventKind, Scales
from intentia_amoris.kernel.embeddings import LocalHashEmbeddingProvider
from intentia_amoris.kernel.engine import IntentiaEternityEngine


async def main():
    engine = IntentiaEternityEngine(LocalHashEmbeddingProvider())
    event = Event(
        actor=ActorRole.SELF,
        kind=EventKind.TEXT,
        content="Даша моє ядро реальності я хочу її ніжно без тиску і на все життя",
    )
    out = await engine.process_event(Scales(), event, ["Даша — ядро реальності Ярослава"])
    print(out)


if __name__ == "__main__":
    asyncio.run(main())
