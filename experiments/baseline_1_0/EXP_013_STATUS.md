# EXP-013 Status

## Experiment

EXP-013 — Controlled State Change

## Status

COMPLETED

## Reproducibility Check

- Tests: 11 passed
- Reference validation: OK
- Reference mappings: 1
- Raw result checksum:

fbbf85150b8d5c58c47bce65d624cefc9d6bdd4ad1978aee3a113930dcfddae7

## Experimental Finding

A controlled change in `connection_rate` from 0.98 to 0.90
propagated through:

State
→ Wave
→ Lyapunov
→ Risk
→ Policy
→ Controller

The observed risk, policy, and controller outputs remained unchanged:

LOW
→ MONITOR
→ OBSERVE

## Interpretation

The experiment demonstrates reproducible propagation through the
implemented computational pipeline.

It does not establish causal improvement in stability or imply that
the changed state is preferable.

## Validation Boundary

The Quran reference layer is used as structured reference metadata.
The experimental result is independently measured from the computational
model and is not treated as proof of the reference interpretation.
