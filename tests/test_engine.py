import pytest

from intentia_amoris.domain import ActorRole, Event, EventKind, Scales
from intentia_amoris.kernel.embeddings import LocalHashEmbeddingProvider
from intentia_amoris.kernel.engine import IntentiaEternityEngine


@pytest.mark.asyncio
async def test_engine_outputs_advice():
    engine = IntentiaEternityEngine(LocalHashEmbeddingProvider(dim=128))
    event = Event(
        actor=ActorRole.SELF,
        kind=EventKind.TEXT,
        content="я дуже хочу але хочу без тиску і з повагою",
    )
    out = await engine.process_event(Scales(), event, ["конституція любові: темп важливіший за напір"])
    assert not out["blocked"]
    assert out["advice"]
    assert out["questions"]
    assert out["scales"]
