from __future__ import annotations

from intentia_amoris.domain import Scales
from intentia_amoris.kernel.value_functions_v4 import decision_policy, omega_value_function


def main() -> None:
    value = omega_value_function(
        Scales(trust=0.72, desire=0.81, safety=0.68, reciprocity=0.70, clarity=0.66, autonomy=0.76),
        {
            "partner_signal": 0.71,
            "retrieval_quality": 0.82,
            "archive_integrity": 0.88,
            "consent_freshness": 0.70,
            "privacy_quality": 0.86,
        },
    )
    print(value.as_dict())
    print(decision_policy(value))


if __name__ == "__main__":
    main()
