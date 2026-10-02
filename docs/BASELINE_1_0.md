# Wave Path 2.0 — Baseline 1.0

## Status

Baseline established after successful end-to-end validation.

## Main Repository

HEAD:
77d0abe Add controller feedback state trace test

## Validation

Quran reference loader:
- interface: wave-path-quran-reference
- version: 1.0
- mappings: 1
- validation: OK

Test suite:
- tests/quran_core/
- result: 11 passed

## Operational Trace

Reference
→ Hypothesis
→ Observation
→ State
→ State Update
→ Wave
→ Lyapunov
→ Risk
→ Policy
→ Controller
→ Feedback
→ State

## Repository Boundary

The Quran reference layer is maintained as an independent Git repository:

wave-path-quran-reference/

The main repository consumes its exported reference data through:

wave-path-quran-reference/integration/adapter/reference_export.json

## Methodological Boundary

The reference layer provides structured textual and conceptual metadata.

It does not directly control runtime state, telemetry, Lyapunov calculations,
risk decisions, policy execution, or controller actions.

Empirical measurements and experimental conclusions remain independently
defined, reproducible, and auditable.

## Baseline Rule

No experimental conclusion is considered validated merely because it agrees
with the reference layer. Experimental validation must be based on measurable
and reproducible results.
