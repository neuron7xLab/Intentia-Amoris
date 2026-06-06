from intentia_amoris.memory.state_contract import after, same_seen, value_of


def test_state_sequence_helpers() -> None:
    assert value_of(None) == 0
    assert after(None) == 1
    assert after(7) == 8
    assert same_seen(stored=3, seen=3)
    assert not same_seen(stored=4, seen=3)
