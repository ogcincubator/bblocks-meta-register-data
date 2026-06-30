#!/usr/bin/env python3
"""Compile registers/*/registers.yaml into a flat index.json."""

import json
import sys
from pathlib import Path

import yaml


def compile_index(registers_root: Path) -> dict:
    index = {}
    errors = []

    for registers_file in sorted(registers_root.glob("*/registers.yaml")):
        org = registers_file.parent.name
        try:
            data = yaml.safe_load(registers_file.read_text())
        except yaml.YAMLError as e:
            errors.append(f"{registers_file}: invalid YAML — {e}")
            continue

        entries = data.get("registers")
        if not isinstance(entries, dict):
            errors.append(f"{registers_file}: 'registers' must be a mapping")
            continue

        for name, url in entries.items():
            if not isinstance(url, str) or not url.startswith("http"):
                errors.append(f"{registers_file}: entry '{name}' has invalid URL: {url!r}")
                continue
            key = f"@{org}/{name}"
            if key in index:
                errors.append(f"{registers_file}: duplicate key {key!r}")
                continue
            index[key] = url

    return index, errors


def main():
    root = Path(__file__).parent.parent / "registers"
    if not root.is_dir():
        print(f"ERROR: registers directory not found at {root}", file=sys.stderr)
        sys.exit(1)

    index, errors = compile_index(root)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    out = Path(__file__).parent.parent / "index.json"
    out.write_text(json.dumps(index, indent=2) + "\n")
    print(f"Wrote {len(index)} entries to {out}")


if __name__ == "__main__":
    main()
