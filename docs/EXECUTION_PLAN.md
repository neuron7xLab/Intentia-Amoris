# Execution Plan

Priority: smallest reproducible gate first.

## Selected patch

Add `scripts/verify_all.sh` as the local executor gate.

## Scope

- compile source
- run tests
- parse JSON audit artifacts when present
- emit deterministic PASS marker

## Non-scope

- no framework rewrite
- no API surface change
- no cosmetic refactor
