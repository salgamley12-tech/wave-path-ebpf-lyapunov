# Wave Path 2.0 — Experiment Index

## Baseline

Baseline 1.0:
- Commit: 08da57b
- Test suite: 11 passed
- Reference validation: OK

## EXP-013

Title:
Controlled State Change

Status:
COMPLETED

Definition commit:
8c624d2

Completion commit:
2bf628b

Reproducibility status commit:
e9f2c29

Raw results:
EXP_013_results.txt

SHA256:
fbbf85150b8d5c58c47bce65d624cefc9d6bdd4ad1978aee3a113930dcfddae7

Main observation:
A controlled change in connection_rate propagated through the implemented
State → Wave → Lyapunov → Risk → Policy → Controller pipeline.

## EXP-014

Title:
Risk Boundary

Status:
COMPLETED

Definition commit:
2926089

Completion commit:
8d68e9b

Raw results:
EXP_014_results.txt

SHA256:
4e9895351e088eef01bde119a8bb45ccbcba8fe4141a5f7ba87c0a9ac9f7b426

Main observation:
The implemented risk classifier produced LOW, LOW, MEDIUM, and HIGH
for the four tested dV/dt cases.

## Methodological Boundary

These experiments validate behavior of the implemented computational
pipeline.

They do not establish universal scientific laws or causal conclusions
beyond the tested model and conditions.
## EXP-015

Title:
Feedback State Loop

Status:
COMPLETED

Definition commit:
2dff0f6

Completion commit:
16ca0ec

Raw results:
EXP_015_results.txt

Main observation:
When state_updated is false, the implemented feedback layer preserves
the existing State without modification.

Methodological boundary:
This validates the implemented software behavior only. It does not
establish a universal feedback-control law.
## EXP-015

Title:
Feedback State Loop

Status:
COMPLETED

Definition commit:
2dff0f6

Completion commit:
16ca0ec

Raw results:
EXP_015_results.txt

Main observation:
When state_updated is false, the implemented feedback layer preserves
the existing State without modification.

Methodological boundary:
This validates the implemented software behavior only. It does not
establish a universal feedback-control law.
