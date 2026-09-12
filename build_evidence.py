#!/usr/bin/env python3
"""Build deterministic evidence records for Project 15."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from independent_verify import verify as independent_verify
from verify_code import verify_path


ROOT = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def fixture_record(relative: str, expected_size: int) -> dict[str, object]:
    path = ROOT / relative
    primary = verify_path(path, expected_size=expected_size)
    independent = independent_verify(path, expected_size)
    for key in (
        "code_size",
        "exact_covering_radius",
        "distance_distribution",
        "hole_count",
        "holes",
        "valid",
    ):
        if primary[key] != independent[key]:
            raise ValueError(f"verifiers disagree on {relative}: {key}")
    return {
        "source": path.name,
        "sha256": primary["sha256"],
        "code_size": primary["code_size"],
        "exact_covering_radius": primary["exact_covering_radius"],
        "distance_distribution": primary["distance_distribution"],
        "pair_distance_distribution": primary[
            "pair_distance_distribution"
        ],
        "diameter": primary["diameter"],
        "hole_count": primary["hole_count"],
        "holes": primary["holes"],
        "valid": primary["valid"],
        "independent_python_verifier_agrees": True,
        "direct_cpp_verifier_expected": {
            "exact_covering_radius": primary["exact_covering_radius"],
            "hole_count": primary["hole_count"],
        },
    }


def records() -> dict[str, object]:
    construction = fixture_record("data/code-27.txt", 27)
    near_cover = fixture_record("data/near-cover-26-5-holes.txt", 26)
    source = json.loads(
        (ROOT / "data" / "audited-bound-record.json").read_text(
            encoding="ascii"
        )
    )
    return {
        "construction-verification.json": {
            "schema_version": 1,
            "generated_at": "2026-09-11",
            "parameter": "K_4(8,4)",
            "starting_interval": "13 <= K_4(8,4) <= 28",
            "improved_interval": "13 <= K_4(8,4) <= 27",
            "computed": construction,
            "verification_paths": [
                "integer exhaustive Python verifier",
                "string exhaustive Python verifier",
                "direct-distance C++ verifier",
            ],
            "global_upper_bound_improved": True,
        },
        "near-cover-analysis.json": {
            "schema_version": 1,
            "generated_at": "2026-09-11",
            "parameter": "K_4(8,4)",
            "computed": near_cover,
            "claim_boundary": (
                "The retained 26-word candidate is not a covering code. "
                "Its five holes and all failed searches are not lower-bound "
                "evidence."
            ),
        },
        "source-audit.json": {
            "schema_version": 1,
            "generated_at": "2026-09-11",
            "parameter": "K_4(8,4)",
            "record": source,
            "record_sha256": digest(
                ROOT / "data" / "audited-bound-record.json"
            ),
            "coldcase_source_commit": (
                "56a8cce68ec3f6f406c845f5cc3e51711e5b8294"
            ),
            "bounded_current_review": {
                "large_alphabet_paper": "arXiv:2608.19872",
                "large_alphabet_scope": "q=5 through q=21",
                "lower_bound_paper": "arXiv:2504.01932",
                "equivalent_27_word_result_located": False,
                "limitation": (
                    "The review cannot exclude inaccessible, unpublished, "
                    "unindexed, or later work."
                ),
            },
        },
        "selection-pilot.json": {
            "schema_version": 1,
            "audit_date": "2026-09-11",
            "selected_parameter": "K_4(8,4)",
            "comparison_pilots": [
                {
                    "parameter": "K_4(10,6)",
                    "target_size": 15,
                    "seconds": 45,
                    "best_holes": 24,
                },
                {
                    "parameter": "K_4(9,5)",
                    "target_size": 15,
                    "seconds": 45,
                    "best_holes": 2284,
                },
                {
                    "parameter": "K_4(11,7)",
                    "target_size": 10,
                    "seconds": 45,
                    "best_holes": 3767,
                },
                {
                    "parameter": "K_4(8,4)",
                    "target_size": 27,
                    "seconds_to_cover": 9.77,
                    "best_holes": 0,
                },
            ],
            "size_26_campaign": {
                "runs": 5,
                "budgets_seconds": [90, 120, 120, 120, 120],
                "best_holes": 5,
                "runs_at_best": 5,
                "proof_value": "none",
            },
            "publication_decision": "hold",
            "publication_reason": (
                "The mathematical significance gate passes, but external "
                "review, an immutable release, and paper-inclusive archival "
                "remain pending."
            ),
            "publication_readiness_observed_at": "2026-09-12",
            "public_repository": {
                "repository": (
                    "ruturajr-raval/"
                    "quaternary-covering-code-8-4-upper-bound"
                ),
                "visibility": "public",
                "default_branch": "main",
                "verified": True,
            },
            "hosted_ci": {
                "workflow": "ci",
                "bootstrap_run_id": 34660831919,
                "commit": (
                    "d9549e699f63050bc2ea16033b842b2b89da44e6"
                ),
                "conclusion": "success",
                "jobs": ["verify", "paper"],
            },
            "external_review": {
                "repository_issue": 1,
                "status": "open",
                "gate_passed": False,
            },
            "required_release_order": [
                "public repository",
                "immutable paper-inclusive release",
                "Zenodo deposit",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    values = records()
    if arguments.write:
        evidence = ROOT / "evidence"
        evidence.mkdir(exist_ok=True)
        for name, value in values.items():
            (evidence / name).write_text(
                json.dumps(value, indent=2, sort_keys=True) + "\n",
                encoding="ascii",
            )
    print("verified_27_word_code=true")
    print("verified_26_word_holes=5")
    print("improved_upper_bound=27")
    print("publication_decision=hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
