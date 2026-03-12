import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from minimake import create_clean_env

env = create_clean_env()
assert env is not None, "create_clean_env should return a dict"

assert "PATH" in env, "PATH should be set"
assert "/usr/bin" in env["PATH"] or "/bin" in env["PATH"], f"PATH should contain system dirs, got {env['PATH']}"

assert env.get("SOURCE_DATE_EPOCH") == "0", f"SOURCE_DATE_EPOCH should be '0', got {env.get('SOURCE_DATE_EPOCH')}"

assert env.get("TZ") == "UTC", f"TZ should be 'UTC', got {env.get('TZ')}"

assert "LANG" in env or "LC_ALL" in env, "LANG or LC_ALL should be set"

print("OK: create_clean_env works correctly")
