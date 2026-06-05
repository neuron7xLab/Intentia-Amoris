import pytest

from intentia_amoris.kernel.embeddings import LocalHashEmbeddingProvider, cosine


@pytest.mark.asyncio
async def test_local_embedding_is_stable():
    provider = LocalHashEmbeddingProvider(dim=64)
    a = await provider.embed("довіра ніжність безпека")
    b = await provider.embed("довіра ніжність безпека")
    assert a == b
    assert len(a) == 64
    assert cosine(a, b) > 0.99
