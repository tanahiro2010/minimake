#!/bin/bash
set -e

cat > build_parallel.json << 'EOF'
{
  "targets": {
    "a.txt": {"deps": [], "inputs": [], "command": "echo a > a.txt"},
    "b.txt": {"deps": [], "inputs": [], "command": "echo b > b.txt"},
    "c.txt": {"deps": [], "inputs": [], "command": "echo c > c.txt"},
    "result.txt": {
      "deps": ["a.txt", "b.txt", "c.txt"],
      "inputs": ["a.txt", "b.txt", "c.txt"],
      "command": "cat a.txt b.txt c.txt > result.txt"
    }
  }
}
EOF

rm -f a.txt b.txt c.txt result.txt

python ../src/minimake.py --parallel result.txt --file build_parallel.json 2>&1 | tee output.txt

test -f a.txt
test -f b.txt
test -f c.txt
test -f result.txt

grep -q "Build levels: 2" output.txt
grep -q "Level 0" output.txt
grep -q "Level 1" output.txt
grep -q "Build completed successfully" output.txt

rm -f a.txt b.txt c.txt result.txt build_parallel.json output.txt
echo "OK: parallel build works correctly"
