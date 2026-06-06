from intentia_amoris.reasoning.gates import GATES, run_gates


def test_gate_catalog_has_eleven_items():
    assert len(GATES) == 11
    assert GATES[0] == "G1"
    assert GATES[-1] == "G11"


def test_gate_runner_accepts_complete_catalog():
    ok, rows = run_gates({gate: (lambda: True) for gate in GATES})
    assert ok is True
    assert len(rows) == 11
