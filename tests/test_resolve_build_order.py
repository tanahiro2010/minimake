import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from minimake import load_build_file, resolve_build_order

config = load_build_file("build.json")

order = resolve_build_order(config, "hello")
assert order is not None, "resolve_build_order returned None"
assert "hello.o" in order, "hello.o not in build order"
assert "hello" in order, "hello not in build order"
assert order.index("hello.o") < order.index("hello"), "hello.o should come before hello"
print("OK: resolve_build_order works correctly")
