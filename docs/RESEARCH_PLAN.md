# Research Plan

## Immediate Construction Route

1. Generate independent 27-word covers rather than overfitting one fixture.
2. Delete one center and use multiword repair on each resulting 26-word code.
3. Target fewer than five holes before extending run time.
4. Verify every improvement through all three exhaustive paths.

## Exact Route

A lower-bound claim requires a complete finite reduction and independently
checked proof objects. Search failures and timeouts do not count.

## Acceptance Thresholds

- A verified 26-word cover is an immediate new upper-bound improvement.
- A strict improvement below five holes is meaningful private research
  progress but not a new global bound.
- A complete checked exclusion below a specified size is a lower-bound result.

## Kill Criterion

Place additional construction search on hold if a bounded campaign produces
neither a 26-word cover nor a strict improvement over five holes. Preserve
the verified 27-word theorem regardless.

## Publication Sequence

The public repository and initial hosted replay now pass. Resolve external
review issue `#1`, refresh prior art at the release date, and reverify the
final release commit before creating an immutable paper-inclusive release.
The deterministic PDF, paper-source archive, and checksums are prepared as
candidate assets. Create the Zenodo deposit only after the immutable release
exists and its assets are final.
