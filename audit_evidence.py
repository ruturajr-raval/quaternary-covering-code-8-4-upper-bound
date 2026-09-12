#!/usr/bin/env python3
"""Recompute Project 15 evidence and reject claim-scope drift."""

from __future__ import annotations

import json
from pathlib import Path

import build_evidence


ROOT = Path(__file__).resolve().parent


def main() -> int:
    expected = build_evidence.records()
    for name, value in expected.items():
        observed = json.loads(
            (ROOT / "evidence" / name).read_text(encoding="ascii")
        )
        if observed != value:
            raise ValueError(f"evidence record changed: {name}")
    construction = expected["construction-verification.json"]
    if construction["global_upper_bound_improved"] is not True:
        raise ValueError("construction record lost the bound improvement")
    if construction["computed"]["exact_covering_radius"] != 4:
        raise ValueError("construction radius changed")
    near = expected["near-cover-analysis.json"]
    if near["computed"]["hole_count"] != 5:
        raise ValueError("near-cover frontier changed")
    selection = expected["selection-pilot.json"]
    if selection["publication_decision"] != "hold":
        raise ValueError("publication decision changed")
    if selection["public_repository"]["verified"] is not True:
        raise ValueError("public repository verification changed")
    if selection["hosted_ci"]["conclusion"] != "success":
        raise ValueError("hosted CI status changed")
    if selection["external_review"] != {
        "repository_issue": 1,
        "status": "open",
        "gate_passed": False,
    }:
        raise ValueError("external review status changed")
    if selection["paper_inclusive_archive"] != {
        "version": "v0.1.0",
        "asset_count": 3,
        "deterministic_double_build_passes": True,
        "ready": True,
        "published": False,
    }:
        raise ValueError("paper-inclusive archive status changed")
    if selection["required_release_order"] != [
        "public repository",
        "immutable paper-inclusive release",
        "Zenodo deposit",
    ]:
        raise ValueError("release ordering changed")
    print("verified_27_word_code=true")
    print("verified_26_word_holes=5")
    print("improved_interval=13..27")
    print("publication_decision=hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
