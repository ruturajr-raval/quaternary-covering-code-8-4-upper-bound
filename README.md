# Quaternary Covering Code `K_4(8,4)` Upper-Bound Workbench

## Project Overview

| Field | Value |
| --- | --- |
| Author | Ruturaj R Raval |
| Affiliation | Independent Researcher |
| ORCID | [0000-0003-4930-8981](https://orcid.org/0000-0003-4930-8981) |
| Field | Coding theory, exhaustive verification, and finite construction search |
| Problem | Determine the exact value of `K_4(8,4)` |
| Current result | A verified 27-word code proves `K_4(8,4) <= 27`; one retained 26-word candidate has exactly five holes |
| Result type | Project-original verified upper-bound improvement relative to the audited table frontier |
| Release | not yet released |
| Version DOI | not yet assigned |
| Concept DOI | not yet assigned |
| License | MIT |

This package studies the minimum size `K_4(8,4)` of a quaternary length-8
code whose Hamming balls of radius 4 cover all `4^8 = 65,536` words. The
audited starting interval was

```text
13 <= K_4(8,4) <= 28.
```

The retained 27-word code has exact covering radius 4 under three exhaustive
verifier paths. It therefore narrows the audited interval to

```text
13 <= K_4(8,4) <= 27.
```

## Problem And Background

A `q`-ary covering code of length `n` and radius `R` is a set of words such
that every word in the ambient Hamming space lies within Hamming distance at
most `R` of at least one selected center. The covering number `K_q(n,R)` is
the least possible number of centers.

The finite covering-code problem and this notation are recorded in the 1997
monograph *Covering Codes*, which supplies the historical source used here.

For `q=4`, `n=8`, and `R=4`, one radius-4 ball contains

```text
sum_{i=0}^4 binom(8,i) 3^i = 7,459
```

words. The sphere-covering count alone gives a weak lower bound because the
balls overlap. Exact construction search and exhaustive verification are
therefore central for this cell.

## Starting Frontier And Longstanding Gap

The dated source audit on 2026-09-11 reconstructed the frozen Keri table cell

```text
w 13-28 m
```

for `K_4(8,4)`. The table attributes the lower bound 13 to Keri's 2008 work
and the upper bound 28 to Ostergard's 1991 construction work. The frozen
machine-readable table record has SHA-256
`7efb0122b7d6a60302194455953591c3e9842a8e7eff9b6f8f49858de3f7522c`.

The 2025-2026 semidefinite lower-bound work retains 13 for this cell. The
2026 large-alphabet upper-bound campaign treats alphabets 5 through 21 and
does not supersede this quaternary entry. No accessible primary-source
27-word construction was located in the bounded current review.

This establishes the audited source frontier, not universal priority. The
review cannot exclude inaccessible, unpublished, unindexed, or later work.
The upper bound 28 had remained in the located table lineage for about
35 years.

## Main Result

Project 15 independently verifies that the retained fixture
`data/code-27.txt` contains 27 distinct quaternary length-8 words and has
exact covering radius 4 over the complete ambient space. The prior audited
upper bound was 28. This result establishes an independently checked
construction.

Therefore:

```text
K_4(8,4) <= 27.
```

Combined with the audited lower bound, the supported interval is

```text
13 <= K_4(8,4) <= 27.
```

A separate retained 26-word candidate has exact covering radius 5 and leaves
exactly five radius-4 holes. It is a construction frontier, not a covering
code and not lower-bound evidence.

## Method And Proof Architecture

The candidate was found during a comparative construction screen using the
third-party `coldcase` engine at source commit
`56a8cce68ec3f6f406c845f5cc3e51711e5b8294`. The search compared one-word
improvement targets for four quaternary cells. The `K_4(8,4)` size-27 run
found a cover after 9.77 seconds; the other three target runs remained
uncovered within their 45-second budgets.

The mathematical result does not trust the search engine's internal score.
The emitted code is treated only as an untrusted candidate and is re-read
from disk by:

1. an integer-tuple Python verifier that exhaustively enumerates every
   ambient word and computes its nearest-center distance;
2. a separately implemented string-based Python verifier with independent
   parsing and loops; and
3. a C++ verifier that decodes each base-4 integer and computes all direct
   Hamming distances.

Five subsequent size-26 campaigns, with budgets of 90 to 120 seconds,
independently retained a five-hole frontier. Failed construction searches
have no proof value.

## Verification And Evidence

All three verifier paths report exact covering radius 4 and zero holes for
the 27-word code. The independent string-based Python implementation agrees
with the primary integer implementation on the complete nearest-distance
distribution, and the C++ verifier supplies a third direct check:

```text
distance 0:     27
distance 1:    648
distance 2:  6,750
distance 3: 33,100
distance 4: 25,011
```

The construction fixture SHA-256 is
`1f83a962906943f04be960e275138ab7508d4a45cec62e58730504b873363b39`.

The 26-word fixture has SHA-256
`a221b79bce498a0a44a95f76640111315e838872f4e7b1beec5ed23c3909abd4`
and exactly these five holes:

```text
02131221
12013220
13332010
20222020
33310232
```

The evidence records bind the fixture hashes, complete distance
distributions, pair-distance distributions, source audit, search scope,
claim boundary, and release ordering. Tests include malformed-symbol and
duplicate-codeword rejection.

## Reproduction

Use Python 3.9 or later, Make, Git, and a C++17 compiler. The verification
code has no third-party package dependency. A commodity workstation is
sufficient; the complete ambient space has only 65,536 words.

Run the full local gate:

```bash
make check
```

Run the construction verifiers separately:

```bash
python3 verify_code.py data/code-27.txt --expected-size 27
python3 independent_verify.py data/code-27.txt --expected-size 27
make cpp
```

Inspect the 26-word frontier:

```bash
python3 analyze_near_cover.py data/near-cover-26-5-holes.txt
```

The search campaign is not required to verify the theorem. The committed
code fixture and exhaustive verifiers are the trust boundary.

## Claims

The supported claim is:

```text
The retained 27-word quaternary length-8 code has exact covering radius 4
under two independent exhaustive Python implementations and a separately
written direct-distance C++ verifier. Therefore K_4(8,4) <= 27, improving
the audited upper bound 28 by one. The retained 26-word candidate has exact
covering radius 5 and five radius-4 holes.
```

The starting interval, table row, lower bound, and prior 28-word upper bound
are attributed prior work. The 27-word fixture, independent verification
package, evidence, and five-hole frontier are Project 15 work.

## Limitations And Nonclaims

This package does not establish a 26-word covering code, improve the lower
bound 13, or determine the exact value of `K_4(8,4)`. It does not prove that
27 is optimal and does not classify all 27-word codes.

The five-hole candidate and every failed search are not exclusion evidence.
The bounded prior-art review does not prove universal novelty or priority.
External mathematical review and peer review remain absent. No public
repository, tagged release, Zenodo archive, DOI, or dissemination event is
claimed.

## Significance And Use

The construction reduces a long-standing audited upper bound by one with a
small artifact that can be checked exhaustively in under a second on a
commodity workstation. The fixture is useful as a regression target for
covering-code search, local improvement, symmetry reduction, integer
programming, SAT, and heuristic optimization.

The result changes one global table upper bound relative to the audited
frontier. It does not settle the cell or imply a general asymptotic
improvement.

## Remaining Work And Future Directions

The remaining limitation is that no 26-word cover or matching lower-bound
certificate is known here. The next route is a verified 26-word cover. The retained
five-hole code should be attacked by multiword replacements, orbit-aware
repair, and deletion-repair from independently generated 27-word covers.

A proof route would require a complete, independently audited exclusion for
all codes below a stated size. Search timeouts are not acceptable evidence.

Before publication, repeat the prior-art review, obtain external mathematical
review, preserve the passing paper build and visual inspection at the release
commit, and pass clean hosted replay. Place further construction search on
hold if a bounded campaign neither finds a 26-word cover nor improves the
five-hole frontier.

## Repository Layout

- `verify_code.py` is the primary integer exhaustive verifier.
- `independent_verify.py` is the separate string-based verifier.
- `verify_direct.cpp` is the direct-distance C++ verifier.
- `analyze_near_cover.py` reports exact holes and distance distributions.
- `data/` contains the 27-word code, five-hole 26-word frontier, and audited
  source record.
- `evidence/` contains construction, frontier, source, and screening records.
- `tests/` contains verifier, mutation, and evidence tests.
- `docs/` contains the claim ledger, prior-art audit, reproducibility guide,
  and research plan.
- `research/` contains the machine-readable claim and release gate.
- `paper/` contains the technical report source and deferred-submission
  metadata.

## Publication Citation And Archive

Release status: not yet released. Version DOI: not yet assigned. Concept DOI:
not yet assigned.

The mathematical significance gate passes locally, but the publication gate
remains on hold. No public result repository currently exists. The required
order is:

1. create and verify the public result repository;
2. create an immutable paper-inclusive release from an audited commit; and
3. deposit the byte-matching release set in Zenodo and verify the DOI record.

Zenodo must not precede the public repository and immutable release.

## Authorship

Ruturaj R Raval, Independent Researcher.

ORCID: `0000-0003-4930-8981`.

## Licensing And Provenance

Project-original source code and documentation are licensed under MIT. The
27-word code and 26-word near-cover were generated during the dated screening
campaign with third-party `coldcase` search engines retained outside this
package. Those engines and their upstream components retain their own
licenses.

The covering-code definition, table frontier, source attributions, and prior
bounds are not claimed as original. The package contains a derived
machine-readable source record rather than redistributing the third-party
table PDF.

## References

1. G. Cohen, I. Honkala, S. Litsyn, and A. Lobstein, *Covering Codes*,
   North-Holland, 1997.
2. G. Keri, covering-code tables and bibliography, frozen 2011 and audited
   2026-09-11.
3. P. R. J. Ostergard, construction work attributed by the Keri table for the
   prior `K_4(8,4) <= 28` bound, 1991.
4. G. Keri, lower-bound work attributed by the table for
   `K_4(8,4) >= 13`, 2008.
5. D. Gijswijt and S. Polak, "Semidefinite lower bounds for covering codes,"
   arXiv:2504.01932, revised 2026.
6. Mapika, "New upper bounds for covering codes," arXiv:2608.19872, 2026.
7. Mapika, `coldcase`, source commit
   `56a8cce68ec3f6f406c845f5cc3e51711e5b8294`, audited 2026-09-11.
