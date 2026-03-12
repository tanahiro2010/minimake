import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from minimake import load_build_file, build_target

config = load_build_file("build.json")

result = build_target(config, "nonexistent")
assert not result, "build_target should return False for unknown target"
print("OK: Unknown target handling works correctly")
