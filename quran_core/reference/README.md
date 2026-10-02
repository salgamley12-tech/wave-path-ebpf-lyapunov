# Quran Reference Integration

This directory defines the integration boundary between
Wave Path 2.0 and the Quran Reference repository.

Reference repository:

../wave-path-quran-reference

Export interface:

../wave-path-quran-reference/integration/adapter/reference_export.json

Integration flow:

Quran Reference
→ Concept
→ Rule
→ Hypothesis
→ Variable
→ Indicator
→ Measurement
→ Validation
→ Wave Path observation/model layers

Boundary:

The reference layer does not directly control runtime state,
policy, risk, or controller actions.
