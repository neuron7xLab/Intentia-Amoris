from intentia_amoris.consent import ConsentGrant, ConsentLedger, ConsentLevel


def test_matching_full_grant_permits_access() -> None:
    ledger = ConsentLedger([
        ConsentGrant(
            subject_id="alpha",
            recipient_id="beta",
            stream="hrv",
            purpose="repair",
            level=ConsentLevel.FULL,
        )
    ])

    decision = ledger.decision(
        subject_id="alpha",
        recipient_id="beta",
        stream="hrv",
