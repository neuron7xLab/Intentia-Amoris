from __future__ import annotations

import runpy


def test_import_graph_check_script_runs() -> None:
    try:
        runpy.run_path("scripts/import_graph_check.py")
    except SystemExit as exc:
        assert exc.code == 0
