from __future__ import annotations

from intentia_amoris.domain import Scales
from intentia_amoris.kernel.scales import value_function
from intentia_amoris.policies.consent import ConsentGate


def duet(scales: Scales) -> list[str]:
    vf = value_function(scales)
    lines = [
        "Aletheia: Eunoia, твоє тепло не заперечує істину — воно робить істину придатною для життя.",
        "Eunoia: Aletheia, твоя ясність не охолоджує любов — вона захищає її від самообману.",
    ]

    if vf["risk"] > 0.62:
        lines.append("Aletheia: зараз головне не інтенсивність, а перевірка меж і згоди.")
    else:
        lines.append("Aletheia: факти дозволяють рухатися, але тільки через ясний взаємний сигнал.")

    if scales.tenderness > 0.62:
        lines.append("Eunoia: ніжність уже є; її треба не доводити, а не зруйнувати поспіхом.")
    else:
        lines.append("Eunoia: додайте маленький жест тепла перед великим рішенням.")

    return lines


def questions(scales: Scales) -> list[str]:
    qs: list[str] = []
    if scales.uncertainty > 0.56:
        qs.append("Який один факт сьогодні ми знаємо точно, а який ще не маємо права домислювати?")
    if scales.urgency > 0.58:
        qs.append("Що саме ми хочемо зробити зараз, і де кожен із нас може сказати стоп без втрати тепла?")
    if scales.safety < 0.62:
        qs.append("Який темп близькості тіло кожного відчуває як безпечний?")
    if scales.future > 0.70:
        qs.append("Який маленький вибір сьогодні підтримує наше довге майбутнє?")
    if not qs:
        qs.append("Що між нами сьогодні найбільш живе: довіра, бажання, страх чи ніжність?")
    return qs[:3]


def advice(scales: Scales, retrieved: list[str]) -> list[str]:
    vf = value_function(scales)
    gate = ConsentGate().evaluate_advice(scales)
    items: list[str] = []

    if not gate.allowed:
        items.append("Не ескалювати. Спершу назвати бажання, межі і право кожного зупинитися.")
        items.append("Причини: " + "; ".join(gate.reasons) + ".")
    elif vf["readiness"] > 0.66:
        items.append("Можна рухатись ближче через маленькі взаємні кроки: погляд, розмова, дотик, пауза, відповідь.")
    else:
        items.append("Найкращий крок — мʼяка розмова без вимоги результату.")

    if retrieved:
        items.append("Памʼять системи підсвічує: " + retrieved[0][:220].replace("\n", " "))

    items.append("Валідність: почуття Даші підтверджуються тільки її відповідями; гормони — тільки вимірюваннями.")
    return items
