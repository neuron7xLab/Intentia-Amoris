from intentia_amoris.reasoning.entropy import entropy_delta, shannon_bits


def test_empty_text_entropy_is_zero() -> None:
    assert shannon_bits("") == 0.0


def test_mixed_text_has_more_entropy_than_repeated_text() -> None:
    assert shannon_bits("abcd") > shannon_bits("aaaa")


def test_entropy_delta_matches_direct_difference() -> None:
    old = "aaaa"
    new = "abcd"
    assert entropy_delta(old, new) == shannon_bits(new) - shannon_bits(old)
