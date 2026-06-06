from intentia_amoris.consent import ConsentGrant, ConsentLedger, ConsentLevel


def test_matching_request_returns_true() -> None:
    ledger = ConsentLedger([ConsentGrant("alpha", "beta", "hrv", "repair", ConsentLevel.FULL)])
    assert ledger.permits(subject_id="alpha", recipient_id="beta", stream="hrv", purpose="repair") is True


def test_revoked_request_returns_false() -> None:
    ledger