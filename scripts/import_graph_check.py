from __future__ import annotations

import compileall

ok = compileall.compile_dir("src", quiet=1)
print("import_graph_check PASS" if ok else "import_graph_check FAIL")
raise SystemExit(0 if ok else 1)
