# Reproducibility

## Environment

Use Python 3.9 or later, Make, Git, and a C++17 compiler. No third-party
Python dependency is required.

## Complete Check

Run:

```bash
make check
```

The command runs the unit and mutation tests, verifies the 27-word code and
26-word near-cover through two Python implementations, builds and runs the
C++ verifier on both fixtures, recomputes every evidence record, and checks
the closed-world manifest against Git.

## Individual Checks

```bash
python3 verify_code.py data/code-27.txt --expected-size 27
python3 independent_verify.py data/code-27.txt --expected-size 27
python3 analyze_near_cover.py data/near-cover-26-5-holes.txt
make cpp
python3 audit_evidence.py
```

The search engine is outside the theorem trust boundary. Verification starts
from the committed candidate text and exhaustively computes direct Hamming
distances over all 65,536 ambient words.

## Hosted Replay

The public `ci` workflow runs `make check` on Ubuntu 24.04 with Python
3.13.7 and a C++17 compiler. A separate job installs checksum-pinned Tectonic
0.17.0, rebuilds the technical report, rejects TeX warnings, and uploads the
PDF and build log. Bootstrap run `34660831919` completed successfully on
2026-09-12.

## Expected Resources

The full local gate is CPU-only and completes on a commodity workstation.
The C++ build is temporary under `.tmp-verifier/`.
