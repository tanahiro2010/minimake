import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from minimake import collect_all_includes

import os
os.chdir(Path(__file__).parent.parent / "project")

includes = collect_all_includes("hello.c", ".")

assert "greet.h" in includes, f"Expected 'greet.h' in includes, got {includes}"
assert "config.h" in includes, f"Expected 'config.h' in includes (indirect dependency), got {includes}"

print("OK: collect_all_includes works correctly")
