# Quran Reference Repository Link

The Quran reference layer is maintained as an independent Git repository:

`wave-path-quran-reference`

## Integration Boundary

Main Wave Path repository:

`quran_core/reference/adapter/load_reference.py`

Reference repository export:

`wave-path-quran-reference/integration/adapter/reference_export.json`

## Validation

The main repository integration test validates the exported reference structure:

`tests/quran_core/test_reference_integration.py`

Current validation result:

`1 passed`

## Repository Separation

The Quran reference repository remains an independent Git repository.

It must not be added as ordinary tracked files to the main repository.

A Git submodule or another explicit dependency mechanism may be introduced later
when the reference repository has a stable remote and versioning policy.
