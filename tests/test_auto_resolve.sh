#!/bin/bash
set -e

rm -f hello.o hello

cat > build_no_inputs.json << 'EOF'
{
  "targets": {
    "hello.o": {
      "deps": [],
      "command": "gcc -c -o hello.o hello.c"
    },
    "hello": {
      "deps": ["hello.o"],
      "inputs": ["hello.o"],
      "command": "gcc -o hello hello.o"
    }
  }
}
EOF

python ../src/minimake.py hello --file build_no_inputs.json

sleep 1
touch config.h

python ../src/minimake.py hello --file build_no_inputs.json 2>&1 | tee output.txt
grep -q "Building hello.o" output.txt

rm -f output.txt build_no_inputs.json
echo "OK: auto_resolve_inputs detects header dependencies"
