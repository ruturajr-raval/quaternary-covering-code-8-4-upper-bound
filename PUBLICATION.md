# Publication Dossier

## Release Identity

| Field | Value |
| --- | --- |
| Title | Quaternary Covering Code K_4(8,4) Upper-Bound Workbench |
| Author | Ruturaj R Raval |
| Affiliation | Independent Researcher |
| ORCID | `0000-0003-4930-8981` |
| Candidate version | `v0.1.0` |
| License | MIT |
| Package status | not yet released |

## Claim-Safe Public Summary

A retained 27-word quaternary length-8 code has exact covering radius 4
under three exhaustive verifier paths. It proves `K_4(8,4) <= 27`, improving
the audited upper bound 28 by one. A retained 26-word candidate has exactly
five radius-4 holes and is not a covering code.

## Current Supported Result

The audited starting interval `13 <= K_4(8,4) <= 28` narrows to
`13 <= K_4(8,4) <= 27`. The code fixture is hash-bound and every ambient word
is checked directly.

## Verification And Evidence

The package contains two independent dependency-free Python verifiers, one
separately written C++ direct-distance verifier, deterministic evidence,
mutation tests, and a closed-world manifest. The search engine's internal
claim is not trusted.

## Significance And Reuse

The result improves a located table upper bound attributed to 1991. The small
fixture and exhaustive verifiers provide reusable regression targets for
covering-code construction and exact-search systems.

## Claim Boundary And Limitations

The package does not establish a 26-word code, improve the lower bound,
determine the exact value, prove optimality, or classify all 27-word codes.
Failed searches are not lower-bound evidence. External mathematical review
and peer review remain absent.

## Provenance Boundary

Project-original source and documentation are MIT licensed. The table
frontier and source attributions are prior work. Search fixtures were
generated with third-party engines outside this package.

## Review Status

Local fixture, verifier, evidence, source-scope, claim-boundary, paper-build,
visual-inspection, public-repository, hosted-replay, and deterministic
candidate-asset audits pass. External mathematical review issue `#1` remains
open.

## Archive And Citation

Candidate `v0.1.0` is not released. A deterministic PDF, paper-source archive,
and checksum manifest are reproducible, but no immutable release, Zenodo
archive, version DOI, or concept DOI is claimed.

Public repository verification is complete. The remaining order is an
immutable paper-inclusive release, then a byte-matching Zenodo deposit and
DOI verification.

## Remaining Acceptance Gate

Publication requires release-date prior-art refresh, external mathematical
review, final-commit hosted replay, and an immutable paper-inclusive release.
Zenodo follows that release.
