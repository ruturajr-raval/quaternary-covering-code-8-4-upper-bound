#!/usr/bin/env python3
"""Analyze the retained 26-word K_4(8,4) near-cover."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_code import verify_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("code", type=Path)
    parser.add_argument("--expected-size", type=int, default=26)
    arguments = parser.parse_args()
    try:
        report = verify_path(
            arguments.code,
            expected_size=arguments.expected_size,
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error={error}")
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
