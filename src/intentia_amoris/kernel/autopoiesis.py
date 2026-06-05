from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from intentia_amoris.domain import Scales
from intentia_amoris.kernel.value_functions_v4 import OmegaValue, decision_policy, omega_value_function


@dataclass(slots=True)
class AutopoieticState:
    """
    The system's identity is not a prompt.
    Identity = principles + memory + policies + update rules + revocation.
    """

    generation: int = 0
    scales: Scales = field(default_factory=Scales)
    evidence: dict[str, float] = field(default_factory=dict)
    last_value: dict[str, float] = field(default_factory=dict)
    last_policy: list[str] = field(default_factory=list)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True, slots=True)
class AutopoieticTransition:
    before: dict[str, float]
    after: dict[str, float]
    policy: list[str]
    delta: dict[str, float]
    generation: int


def transition(
    state: AutopoieticState,
    new_scales: Scales,
    evidence: dict[str, float] | None = None,
) -> AutopoieticTransition:
    merged_evidence = dict(state.evidence)
    if evidence:
        merged_evidence.update(evidence)

    before_value = omega_value_function(state.scales, state.evidence).as_dict()
    after_value: OmegaValue = omega_value_function(new_scales, merged_evidence)
    after = after_value.as_dict()
    delta = {k: round(after[k] - before_value.get(k, 0.0), 4) for k in after}

    state.generation += 1
    state.scales = new_scales
    state.evidence = merged_evidence
    state.last_value = after
    state.last_policy = decision_policy(after_value)
    state.updated_at = datetime.now(timezone.utc)

    return AutopoieticTransition(
        before=before_value,
        after=after,
        policy=state.last_policy,
        delta=delta,
        generation=state.generation,
    )
