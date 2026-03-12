#!/bin/bash
set -e

rm -f hello.o hello
rm -rf .minimake-cache

python ../src/minimake.py --cache hello 2>&1 | tee output.txt
grep -q "Building hello.o" output.txt
test -d .minimake-cache

rm -f hello.o hello

python ../src/minimake.py --cache hello 2>&1 | tee output.txt
grep -q "Cache hit: hello.o" output.txt
test -f hello.o

echo '// modified' >> hello.c
python ../src/minimake.py --cache hello 2>&1 | tee output.txt
grep -q "Building hello.o" output.txt
git checkout hello.c

rm -f output.txt
rm -rf .minimake-cache
echo "OK: build cache works correctly"
