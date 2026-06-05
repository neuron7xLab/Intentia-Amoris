import pytest

from intentia_amoris.domain import Scales
from intentia_amoris.kernel.embeddings import LocalHashEmbeddingProvider
from intentia_amoris.kernel.scales import DynamicScalesKernel, value_function


@pytest.mark.asyncio
async def test_dynamic_kernel_updates_scales():
    kernel = DynamicScalesKernel(LocalHashEmbeddingProvider(dim=128))
    out = await kernel.update(
        Scales(),
        "я хочу тебе але не хочу тиснути хочу мʼяко і згодою",
    )
    assert out.new_scales.as_dict() != Scales().as_dict()
    vf = value_function(out.new_scales)
    assert 0 <= vf["risk"] <= 1
    assert 0 <= vf["readiness"] <= 1
