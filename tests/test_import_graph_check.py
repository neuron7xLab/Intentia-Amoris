from __future__ import annotations

import runpy


def test_import_graph_check_script_runs() -> None:
    runpy.run_path("scripts/import_graph_check.py")
