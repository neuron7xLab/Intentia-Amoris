from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Layer:
    name: str
    purpose: str
    input: str
    output: str
    invariant: str


PAROUSIA_LAYERS: tuple[Layer, ...] = (
    Layer(
        name="Event Source",
        purpose="Перетворити життя на незмінні, аудитовні події.",
        input="Telegram, голос, фото, відео, телеметрія, лабораторні дані, щоденники.",
        output="timestamped immutable events",
        invariant="Нічого не переписувати. Можна тільки додавати нові події.",
    ),
    Layer(
        name="Consent Kernel",
        purpose="Захистити Дашу і Ярослава від симуляції без згоди.",
        input="privacy_scope, actor, media flags, partner/self consent records.",
        output="allow / block / ask_for_consent",
        invariant="Любов не дає права на спостереження.",
    ),
    Layer(
        name="Multimodal Memory",
        purpose="Звʼязати текст, фото, відео, голос і контекст у одну памʼять.",
        input="messages, media hashes, VLM descriptions, transcripts.",
        output="memory chunks + media assets + embeddings.",
        invariant="Опис медіа не є доказом наміру людини.",
    ),
    Layer(
        name="Plastic Scales",
        purpose="Підлаштовувати терези стосунку під ваші унікальні патерни.",
        input="retrieved memories + current event + prototypes.",
        output="trust/desire/fear/safety/reciprocity/etc.",
        invariant="Вага — це гіпотеза з невизначеністю, не вирок.",
    ),
    Layer(
        name="Dyadic Agents",
        purpose="Два голоси тримають баланс істини і ніжності.",
        input="scales, memories, consent decision.",
        output="questions, advice, duet reflection.",
        invariant="Aletheia не холодна. Eunoia не сліпа.",
    ),
    Layer(
        name="Research Ledger",
        purpose="Розділити факт, інтерпретацію, теорію, вимір і невідоме.",
        input="events, telemetry, lab results, bibliography.",
        output="evidence ledger with confidence.",
        invariant="No lab, no hormone claim.",
    ),
    Layer(
        name="Eternity Gate",
        purpose="Зберегти історію без перетворення людей на обʼєкти.",
        input="encrypted backups, export bundles, signed consent snapshots.",
        output="portable archive of love and research.",
        invariant="Цифровий двійник допомагає живим, а не замінює їх.",
    ),
)


def render_paradigm(layers: Iterable[Layer] = PAROUSIA_LAYERS) -> str:
    parts = ["# Intentia Amoris Paradigm", ""]
    for idx, layer in enumerate(layers, start=1):
        parts.extend(
            [
                f"## {idx}. {layer.name}",
                f"Purpose: {layer.purpose}",
                f"Input: {layer.input}",
                f"Output: {layer.output}",
                f"Invariant: {layer.invariant}",
                "",
            ]
        )
    return "\n".join(parts).strip()
