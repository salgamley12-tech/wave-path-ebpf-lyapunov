# EXP-015 — Feedback State Loop

## Objective

Test the implemented feedback path from Controller output back toward
the State layer.

## Pipeline

State
→ Wave
→ Lyapunov
→ Risk
→ Policy
→ Controller
→ Feedback
→ State

## Controlled Condition

Use the existing end-to-end baseline state and controller output.

The feedback object records:

- previous action
- observed controller mode
- whether state was updated

## Measurement

Record whether the feedback stage preserves the state when
state_updated is false.

## Expected Boundary

The current implementation defines conservative feedback behavior:

state_updated = false
→ State remains unchanged.

## Validation

The experiment validates only the behavior implemented in the current
software.

It does not establish a universal feedback-control law.

## Reproducibility

The experiment must be executable from the repository with the existing
test suite and produce deterministic results.
