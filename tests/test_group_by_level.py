import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from minimake import group_by_level

result = group_by_level({"a": 0, "b": 0, "c": 1, "d": 2})
assert len(result) == 3, f"Expected 3 levels, got {len(result)}"
assert set(result[0]) == {"a", "b"}, f"Level 0 should be ['a', 'b'], got {result[0]}"
assert set(result[1]) == {"c"}, f"Level 1 should be ['c'], got {result[1]}"
assert set(result[2]) == {"d"}, f"Level 2 should be ['d'], got {result[2]}"

result = group_by_level({})
assert result == [], f"Empty input should return [], got {result}"

print("OK: group_by_level works correctly")
