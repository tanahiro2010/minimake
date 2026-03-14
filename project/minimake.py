import json
import subprocess
import sys
from pathlib import Path


def load_build_file(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def needs_rebuild(config: dict, target: str) -> bool:
    targets = config.get("targets", {})
    target_config = targets[target]

    target_path = Path(target)

    if not target_path.exists():
        return True

    target_mtime = target_path.stat().st_mtime # ターゲットファイルの最終更新時刻

    # TODO: inputs と deps の両方をチェックしてください
    # ヒント:
    # - inputs: target_config.get("inputs", [])
    # - deps: target_config.get("deps", [])
    # - ファイルの mtime が target_mtime より大きければ再ビルドが必要
    for input_f in target_config.get("inputs", []):
        input_path = Path(input_f)
        st_time = input_path.stat().st_mtime # 入力ファイルの最終更新時刻
        if not input_path.exists() or st_time > target_mtime: # もし入力ファイルが存在しないか、入力ファイルの方が新しい場合
            return True # 再ビルドが必要

    for dep in target_config.get("deps", []):
        dep_path = Path(dep)
        st_time = dep_path.stat().st_mtime # 依存ファイルの最終更新時刻
        if not dep_path.exists() or st_time > target_mtime: # もし依存ファイルが存在しないか、依存ファイルの方が新しい場合
            return True # 再ビルドが必要

    return False


def build_target(config: dict, target: str) -> bool:
    targets = config.get("targets", {})

    if target not in targets:
        print(f"Error: Unknown target '{target}'", file=sys.stderr)
        return False

    target_config = targets[target]
    command = target_config.get("command")

    if not needs_rebuild(config, target):
        print(f"Skipping {target} (up to date)")
        return True

    if not command:
        print(f"Error: No command for target '{target}'", file=sys.stderr)
        return False

    print(f"Building {target}...")
    print(f"  $ {command}")

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print(f"Error: Build failed for '{target}'", file=sys.stderr)
        return False

    return True


def resolve_build_order(config: dict, target: str) -> list[str]:
    targets = config.get("targets", {})

    visited = set()
    visiting = set()
    order = []

    def visit(t: str):
        if t in visited:
            return
        if t in visiting:
            raise ValueError(f"Circular dependency detected: {t}")

        if t not in targets:
            raise ValueError(f"Unknown target: {t}")

        visiting.add(t)

        for dep in targets[t].get("deps", []):
            visit(dep)

        visiting.remove(t)
        visited.add(t)
        order.append(t)

    visit(target)
    return order


def build_with_deps(config: dict, target: str) -> bool:
    try:
        order = resolve_build_order(config, target)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

    print(f"Build order: {' -> '.join(order)}")

    for t in order:
        is_build = build_target(config, t)
        print(f"Built {t}: {is_build}")
        if not is_build:
            return False

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: minimake <target>... [--file build_file]", file=sys.stderr)
        sys.exit(1)

    targets = []
    build_file = "build.json"

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--file" and i + 1 < len(sys.argv):
            build_file = sys.argv[i + 1]
            i += 2
        else:
            targets.append(sys.argv[i])
            i += 1

    config = load_build_file(build_file)
    print("config: ", json.dumps(config, indent=2))

    for target in targets:
        if not build_with_deps(config, target):
            sys.exit(1)


if __name__ == "__main__":
    main()
