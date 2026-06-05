from intentia_amoris.importers.chunking import chunk_text


def test_chunking_keeps_text():
    chunks = chunk_text("A\n\nB\n\nC", max_chars=10)
    assert chunks
    assert "A" in chunks[0]
