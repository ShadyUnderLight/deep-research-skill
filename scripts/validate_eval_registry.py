#!/usr/bin/env python3
"""CLI entry point for validating the executable forward-eval registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from eval_registry import DEFAULT_REGISTRY_PATH, EvalRegistryError, load_registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the forward eval registry")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable result")
    args = parser.parse_args(argv)

    try:
        data = load_registry(args.registry)
        result = {"valid": True, "version": data["version"], "case_count": len(data["cases"])}
        code = 0
    except EvalRegistryError as exc:
        result = {"valid": False, "gap_class": "fixture-reference-drift", "error": str(exc)}
        code = 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    elif result["valid"]:
        print(f"Valid eval registry: {result['case_count']} case(s)")
    else:
        print(f"Invalid eval registry: {result['error']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
