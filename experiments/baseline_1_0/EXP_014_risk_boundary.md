# EXP-014 — Risk Boundary

## Objective

Test the implemented Lyapunov-to-risk policy boundary using controlled
values of `V` and `dV/dt`.

## Cases

### Case A — Stable

V = 1.0
dV/dt = -0.1

Expected risk:
LOW

### Case B — Tolerance Boundary

V = 1.0
dV/dt = 0.0

Expected risk:
LOW

### Case C — Positive Deviation

V = 1.0
dV/dt = 0.02

Expected risk:
MEDIUM

### Case D — High Positive Deviation

V = 1.0
dV/dt = 0.10

Expected risk:
HIGH

## Scope

This experiment tests only the implemented risk classification boundary.

It does not claim that these thresholds represent a universal physical,
scientific, or real-world risk standard.

## Status

PLANNED

## Result

Status: COMPLETED

Observed classification:

| Case | V | dV/dt | Stable | Risk |
|---|---:|---:|---|---|
| A_STABLE | 1.0 | -0.10 | True | LOW |
| B_ZERO_DERIVATIVE | 1.0 | 0.00 | True | LOW |
| C_POSITIVE_DEVIATION | 1.0 | 0.02 | False | MEDIUM |
| D_HIGH_POSITIVE_DEVIATION | 1.0 | 0.10 | False | HIGH |

## Interpretation

The experiment confirms the implemented classification behavior at the
tested values.

The thresholds are properties of the current implementation and are not
claimed as universal risk thresholds.
