# Experiment 001 — Integrated Wave Path Runtime

## 1. Purpose

This experiment validates the integrated execution path:

Synthetic Telemetry
→ Window Aggregation
→ State Construction
→ Lyapunov-like Energy
→ Risk Classification
→ Policy Decision
→ Wave Path

The experiment is defensive and synthetic. No real network traffic is generated.

## 2. Experimental Configuration

- Experiment ID: EXP-001
- Samples: 200
- Telemetry source: Synthetic
- Window size: 1.0 second
- Unauthorized events: 51
- Runtime module:
  `experiments.integrated.run`

## 3. Observed Results

```text
samples              = 200
initial_V            = 505000.0
final_V              = 63419.005
path_points          = 200
path_displacement    = 64406.27454681725
unauthorized_events  = 51
