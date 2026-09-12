#!/usr/bin/env python3
"""Primary exhaustive verifier for quaternary length-8 covering codes."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


Q = 4
LENGTH = 8
RADIUS = 4


def parse_code(
    path: Path,
    *,
    expected_size: int | None = None,
) -> tuple[tuple[int, ...], ...]:
    code: list[tuple[int, ...]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="ascii").splitlines(),
        start=1,
    ):
        word = line.split("#", 1)[0].strip()
        if not word:
            continue
        if len(word) != LENGTH or any(symbol not in "0123" for symbol in word):
            raise ValueError(f"{path}:{line_number}: invalid codeword")
        code.append(tuple(int(symbol) for symbol in word))
    if not code:
        raise ValueError("code is empty")
    if len(set(code)) != len(code):
        raise ValueError("duplicate codeword")
    if expected_size is not None and len(code) != expected_size:
        raise ValueError(
            f"expected {expected_size} codewords, found {len(code)}"
        )
    return tuple(code)


def distance(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> int:
    return sum(a != b for a, b in zip(left, right))


def analyze_code(
    code: tuple[tuple[int, ...], ...],
) -> dict[str, object]:
    histogram: Counter[int] = Counter()
    holes: list[str] = []
    for point in itertools.product(range(Q), repeat=LENGTH):
        nearest = min(distance(point, center) for center in code)
        histogram[nearest] += 1
        if nearest > RADIUS:
            holes.append("".join(map(str, point)))
    pair_distances = Counter(
        distance(code[left], code[right])
        for left in range(len(code))
        for right in range(left)
    )
    exact_radius = max(histogram)
    return {
        "q": Q,
        "length": LENGTH,
        "requested_radius": RADIUS,
        "ambient_size": Q**LENGTH,
        "code_size": len(code),
        "exact_covering_radius": exact_radius,
        "distance_distribution": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "pair_distance_distribution": {
            str(key): value for key, value in sorted(pair_distances.items())
        },
        "diameter": max(pair_distances, default=0),
        "hole_count": len(holes),
        "holes": holes,
        "valid": exact_radius <= RADIUS,
    }


def verify_path(
    path: Path,
    *,
    expected_size: int | None = None,
) -> dict[str, object]:
    report = analyze_code(parse_code(path, expected_size=expected_size))
    report["source"] = path.name
    report["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("code", type=Path)
    parser.add_argument("--expected-size", type=int)
    parser.add_argument("--json", type=Path)
    arguments = parser.parse_args()
    try:
        report = verify_path(
            arguments.code,
            expected_size=arguments.expected_size,
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error={error}")
        return 2
    text = json.dumps(report, indent=2, sort_keys=True)
    if arguments.json is not None:
        arguments.json.write_text(text + "\n", encoding="ascii")
    print(text)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
