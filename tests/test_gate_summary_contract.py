from intentia_amoris.reasoning.gate_summary import summarize


def test_summary_counts_rows():
    out = summarize((("G1", True), ("G2", True)))
    assert out == {"ok": True, "total": 2, "done": 2, "score": 1.0}
