# EXP-013 — Controlled State Change

## Objective

Measure how a controlled change in `connection_rate` propagates through:

State
→ Wave
→ Lyapunov
→ Risk
→ Policy
→ Controller

## Baseline State

bytes_rate = 1.0
syscall_rate = 1.0
connection_rate = 0.98
anomaly_score = 0.1

## Controlled Change

Only `connection_rate` is changed:

0.98 → 0.90

All other state variables and wave configuration parameters remain unchanged.

## Observables

- Initial Lyapunov value
- Final Lyapunov value
- Final dV/dt
- Risk level
- Policy action
- Controller mode

## Reproducibility

The experiment uses the existing deterministic Wave Path model
and the existing state-to-wave mapping.

## Interpretation Boundary

This experiment measures propagation of a controlled state change.

It does not by itself establish causality, improved stability,
or superiority of one state over another.

## Status

PLANNED
