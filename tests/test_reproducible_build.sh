#!/bin/bash
set -e

rm -f hello.o hello

python ../src/minimake.py --reproducible hello 2>&1 | tee output.txt
grep -q "reproducible mode" output.txt

test -f hello.o
test -f hello

rm -f output.txt
echo "OK: reproducible build works correctly"
