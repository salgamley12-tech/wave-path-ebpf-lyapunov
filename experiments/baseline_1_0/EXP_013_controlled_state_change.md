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

## Result

Status: COMPLETED

The controlled change propagated through the Wave and Lyapunov layers.

Observed final values:

- Baseline V: 0.16714412656488375
- Changed V: 0.14857479215741945
- Delta V: -0.018569334407464305
- Baseline dV/dt: -0.16813397438264488
- Changed dV/dt: -0.14246816895463477
- Risk: LOW → LOW
- Policy: MONITOR → MONITOR
- Controller: OBSERVE → OBSERVE

## Conclusion Boundary

EXP-013 demonstrates reproducible propagation of a controlled state change
through the existing computational pipeline.

It does not establish causal improvement in stability.

Raw results are stored in:

experiments/baseline_1_0/EXP_013_results.txt
