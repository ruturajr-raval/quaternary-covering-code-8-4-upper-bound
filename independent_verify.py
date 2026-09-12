#!/usr/bin/env python3
"""Independent string-based verifier for K_4(8,4) candidates."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


ALPHABET = "0123"
LENGTH = 8
RADIUS = 4


def read_words(path: Path, expected_size: int | None) -> tuple[str, ...]:
    words: list[str] = []
    for line_number, raw in enumerate(
        path.read_bytes().decode("ascii").splitlines(),
        start=1,
    ):
        word = raw.partition("#")[0].strip()
        if not word:
            continue
        if len(word) != LENGTH or set(word) - set(ALPHABET):
            raise ValueError(f"{path}:{line_number}: malformed word")
        words.append(word)
    if not words:
        raise ValueError("no words found")
    if len(words) != len(set(words)):
        raise ValueError("repeated word")
    if expected_size is not None and len(words) != expected_size:
        raise ValueError("unexpected code size")
    return tuple(words)


def verify(
    path: Path,
    expected_size: int | None = None,
) -> dict[str, object]:
    code = read_words(path, expected_size)
    counts: Counter[int] = Counter()
    holes: list[str] = []
    for symbols in itertools.product(ALPHABET, repeat=LENGTH):
        point = "".join(symbols)
        nearest = min(
            sum(left != right for left, right in zip(point, center))
            for center in code
        )
        counts[nearest] += 1
        if nearest > RADIUS:
            holes.append(point)
    exact_radius = max(counts)
    return {
        "source": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "code_size": len(code),
        "exact_covering_radius": exact_radius,
        "distance_distribution": {
            str(key): value for key, value in sorted(counts.items())
        },
        "hole_count": len(holes),
        "holes": holes,
        "valid": exact_radius <= RADIUS,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("code", type=Path)
    parser.add_argument("--expected-size", type=int)
    parser.add_argument("--allow-invalid", action="store_true")
    arguments = parser.parse_args()
    try:
        report = verify(arguments.code, arguments.expected_size)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error={error}")
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["valid"] or arguments.allow_invalid else 1


if __name__ == "__main__":
    raise SystemExit(main())
