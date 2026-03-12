import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from minimake import compute_cache_key

config = {
    "targets": {
        "test.o": {
            "deps": [],
            "inputs": ["test.c"],
            "command": "gcc -c -o test.o test.c",
        }
    }
}

Path("test.c").write_text("int main() { return 0; }")

key1 = compute_cache_key(config, "test.o", {})
assert key1 is not None, "cache key should not be None"
assert len(key1) == 64, f"cache key should be 64 chars (sha256 hex), got {len(key1)}"

key2 = compute_cache_key(config, "test.o", {})
assert key1 == key2, "same inputs should produce same cache key"

Path("test.c").write_text("int main() { return 1; }")
key3 = compute_cache_key(config, "test.o", {})
assert key1 != key3, "different inputs should produce different cache key"

Path("test.c").unlink()
print("OK: compute_cache_key works correctly")
