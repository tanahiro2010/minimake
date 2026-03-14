import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from project.minimake import parse_includes

with tempfile.NamedTemporaryFile(mode="w", suffix=".c", delete=False) as f:
    f.write('#include <stdio.h>\n')
    f.write('#include "greet.h"\n')
    f.write('#include "config.h"\n')
    f.write('int main() { return 0; }\n')
    temp_path = f.name

includes = parse_includes(temp_path)

assert "greet.h" in includes, f"Expected 'greet.h' in includes, got {includes}"
assert "config.h" in includes, f"Expected 'config.h' in includes, got {includes}"
assert "stdio.h" not in includes, f"System header 'stdio.h' should not be in includes"

Path(temp_path).unlink()
print("OK: parse_includes works correctly")
