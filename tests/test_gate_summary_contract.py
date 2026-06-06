from intentia_amoris.reasoning.gate_summary import summarize


def test_summary_counts_rows():
    out = summarize((("G1", True), ("G2", False)))
    assert out == {"ok": False, "total": 2, "done": 1}
