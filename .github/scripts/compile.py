#!/usr/bin/env python3
"""Compile registers/*/registers.yaml into index.json and orgs.json."""

import argparse
import json
import sys
from pathlib import Path

import jsonschema
import yaml

REGISTERS_SCHEMA = {
    "type": "object",
    "required": ["org", "registers"],
    "additionalProperties": False,
    "properties": {
        "org": {
            "type": "object",
            "required": ["name", "url", "maintainers"],
            "additionalProperties": False,
            "properties": {
                "name": {"type": "string", "minLength": 1},
                "description": {"type": "string", "minLength": 1},
                "url": {
                    "type": "string",
                    "pattern": r"^https?://",
                },
                "maintainers": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["github", "email"],
                        "additionalProperties": False,
                        "properties": {
                            "github": {"type": "string", "minLength": 1},
                            "email": {
                                "type": "string",
                                "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                            },
                        },
                    },
                },
            },
        },
        "registers": {
            "type": "object",
            "minProperties": 1,
            "additionalProperties": {
                "type": "string",
                "pattern": r"^https?://",
            },
        },
    },
}

_validator = jsonschema.Draft7Validator(REGISTERS_SCHEMA)


def compile(registers_root: Path) -> tuple[dict, dict, list[str]]:
    index = {}
    orgs = {}
    errors = []

    for registers_file in sorted(registers_root.glob("*/registers.yaml")):
        org = registers_file.parent.name
        try:
            data = yaml.safe_load(registers_file.read_text())
        except yaml.YAMLError as e:
            errors.append(f"{registers_file}: invalid YAML — {e}")
            continue

        schema_errors = sorted(_validator.iter_errors(data), key=str)
        if schema_errors:
            for err in schema_errors:
                path = " → ".join(str(p) for p in err.absolute_path) or "(root)"
                errors.append(f"{registers_file} [{path}]: {err.message}")
            continue

        for name, url in data["registers"].items():
            key = f"@{org}/{name}"
            if key in index:
                errors.append(f"{registers_file}: duplicate key {key!r}")
                continue
            index[key] = url

        orgs[org] = {
            **data["org"],
            "registers": list(data["registers"].keys()),
        }

    return index, orgs, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate only — do not write output files",
    )
    args = parser.parse_args()

    cwd = Path.cwd()
    root = cwd / "registers"
    if not root.is_dir():
        print(f"ERROR: registers directory not found at {root}", file=sys.stderr)
        sys.exit(1)

    index, orgs, errors = compile(root)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.validate:
        print(f"OK: {len(index)} register entries, {len(orgs)} orgs validated")
        return

    if "@ogc/main" in index:
        index = {"default": index["@ogc/main"], **index}

    (cwd / "index.json").write_text(json.dumps(index, indent=2) + "\n")
    print(f"Wrote {len(index)} entries to index.json")

    (cwd / "orgs.json").write_text(json.dumps(orgs, indent=2) + "\n")
    print(f"Wrote {len(orgs)} orgs to orgs.json")


if __name__ == "__main__":
    main()
