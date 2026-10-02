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
## EXP-016

Title:
Feedback Update Boundary

Status:
COMPLETED

Definition commit:
b13ddf2

Completion commit:
33ad158

Raw results:
EXP_016_results.txt

Main observation:
The current implementation preserves all State field values for both
state_updated=false and state_updated=true.

Methodological boundary:
This validates the behavior of the current implementation only.
Future feedback behavior requires an explicit and measurable state
update rule.

## EXP-017

Title:
Decision Boundary Comparison

Status:
COMPLETED

Definition:
Decision-boundary comparison between the legacy risk classifier and
the current Lyapunov risk assessment using identical inputs.

Cases:
5

Matches:
3

Mismatches:
2

Raw results:
EXP_017_decision_boundary/EXP_017_results.txt

Main observation:
The legacy and current risk classifiers are not semantically equivalent.

The legacy classifier treats any positive dVdt as HIGH and incorporates
anomaly_score.

The current Lyapunov classifier distinguishes MEDIUM and HIGH according
to the implemented dVdt/V boundary and does not currently incorporate
anomaly_score.

Methodological boundary:
EXP-017 validates the existence of an implementation-level decision
boundary difference. It does not establish which classifier is
universally preferable. No production classifier was modified.

## EXP-018

Title:
Risk Input Boundary Comparison

Status:
COMPLETED

Definition:
Comparison of the legacy and current risk paths using identical
Lyapunov values and controlled anomaly_score values.

Cases:
4

Main observation:
The legacy classifier incorporates anomaly_score, while the current
Lyapunov risk assessment does not accept anomaly_score as an independent
input.

Changing anomaly_score while keeping V and dVdt constant changed the
legacy classification but did not change the current classification.

Raw results:
EXP_018_risk_input_boundary/EXP_018_results.txt

Methodological boundary:
EXP-018 validates an implementation-level input boundary.
It does not establish which risk model is universally preferable.
No production classifier was modified.
