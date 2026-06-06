from intentia_amoris.reasoning.gates import GATES, run_gates


def test_gate_catalog_has_eleven_items():
    assert GATES == tuple(f"G{i}" for i in range(1, 12))


def test_gate_runner_accepts_complete_catalog():
    ok, rows = run_gates({gate: (lambda: True) for gate in GATES})
    assert ok is True
    assert len(rows) == 11


def test_gate_runner_marks_missing_item():
    ok, rows = run_gates({"G1": lambda: True})
    assert ok is False
    assert rows[0] == ("G1", True