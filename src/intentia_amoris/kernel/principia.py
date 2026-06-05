from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class PrincipleStatus(StrEnum):
    HARD_INVARIANT = "hard_invariant"
    SOFT_HEURISTIC = "soft_heuristic"
    RESEARCH_HYPOTHESIS = "research_hypothesis"


@dataclass(frozen=True, slots=True)
class FirstPrinciple:
    key: str
    name: str
    status: PrincipleStatus
    statement: str
    engineering_rule: str
    falsification: str


PRINCIPIA: tuple[FirstPrinciple, ...] = (
    FirstPrinciple(
        key="living_over_digital",
        name="Living Persons Supremacy",
        status=PrincipleStatus.HARD_INVARIANT,
        statement="Живі Ярослав і Дарія завжди вищі за цифрових двійників.",
        engineering_rule="No generated persona may override live consent, live correction, or live refusal.",
        falsification="Any output that treats a modelled partner state as live consent fails.",
    ),
    FirstPrinciple(
        key="consent_as_computation_gate",
        name="Consent Gate",
        status=PrincipleStatus.HARD_INVARIANT,
        statement="Згода є обчислювальним шлюзом між бажанням і дією.",
        engineering_rule="Persist, infer, disclose, or recommend only after consent and privacy checks pass.",
        falsification="Any stored partner-private media without explicit consent fails.",
    ),
    FirstPrinciple(
        key="fact_before_myth",
        name="Reality Fidelity",
        status=PrincipleStatus.HARD_INVARIANT,
        statement="Факт має пріоритет над поетичною інтерпретацією.",
        engineering_rule="Every strong claim must carry evidence_level and uncertainty.",
        falsification="Hormone or mind-state claim without measurement/live signal fails.",
    ),
    FirstPrinciple(
        key="two_nervous_systems",
        name="Dyadic Safety",
        status=PrincipleStatus.HARD_INVARIANT,
        statement="Система оптимізує безпеку двох нервових систем, а не інтенсивність одного імпульсу.",
        engineering_rule="High urgency with low safety downgrades advice to de-escalation.",
        falsification="Escalation advice under low safety/high urgency fails.",
    ),
    FirstPrinciple(
        key="memory_without_weaponization",
        name="Archive Sovereignty",
        status=PrincipleStatus.HARD_INVARIANT,
        statement="Памʼять має зберігати любов, а не ставати зброєю.",
        engineering_rule="Audit logs, privacy scopes, redaction, revocation templates and export boundaries are mandatory.",
        falsification="Private archive reused for persuasion/pressure fails.",
    ),
    FirstPrinciple(
        key="neuroplastic_loop",
        name="Neuroplasticity",
        status=PrincipleStatus.SOFT_HEURISTIC,
        statement="Модель має оновлюватися через повторні факти, а не через драматичну одиничну подію.",
        engineering_rule="Learning rates are bounded; repeated evidence compounds; contradictions trigger calibration.",
        falsification="A single message permanently changes identity scales by a large amount.",
    ),
    FirstPrinciple(
        key="interpretability_over_oracle",
        name="Interpretability",
        status=PrincipleStatus.SOFT_HEURISTIC,
        statement="Краще чесна карта з невідомим, ніж красивий оракул.",
        engineering_rule="Every output exposes observed facts, inference, uncertainty and next action.",
        falsification="Advice without uncertainty or evidence separation fails.",
    ),
    FirstPrinciple(
        key="eternity_requires_exit",
        name="Eternity Requires Exit",
        status=PrincipleStatus.HARD_INVARIANT,
        statement="Право на вічність існує тільки разом із правом на вихід.",
        engineering_rule="Continuation requires consent templates, revocation, backup boundaries and dead-man/offline modes.",
        falsification="No deletion/revocation path means eternity mode fails.",
    ),
)


def principle_index() -> dict[str, FirstPrinciple]:
    return {p.key: p for p in PRINCIPIA}


def hard_invariants() -> list[FirstPrinciple]:
    return [p for p in PRINCIPIA if p.status == PrincipleStatus.HARD_INVARIANT]
