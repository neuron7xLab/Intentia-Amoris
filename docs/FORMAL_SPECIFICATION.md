# Formal Specification

## State

```text
S_t = {
  scales,
  memory_index,
  consent_ledger,
  evidence_ledger,
  audit_chain,
  media_manifest,
  telemetry_series
}
```

## Event

```text
E_t = {
  actor,
  kind,
  content,
  source,
  timestamp,
  confidence,
  privacy_scope,
  metadata,
  embedding
}
```

## Transition

```text
S_{t+1} = T(S_t, E_t)
```

Where:

```text
T = consent_gate
  → validation
  → embedding
  → retrieval
  → scale_update
  → value_update
  → scenario_extrapolation
  → audit_append
```

## Hard constraints

```text
C1: no persistence of sensitive partner-private media before consent
C2: no active consent simulation
C3: no hormone claim without measured lab data
C4: no partner mind-state claim without partner signal
C5: no private archive export without both-party authorization
C6: audit chain must detect tampering
C7: production/staging fails closed without secrets
```

## Output contract

Every meaningful output must expose:

```text
observed_facts
retrieved_memories
inferred_states
uncertainty
value_function
intentia_value
scenario_extrapolation
questions
advice
```

## Falsification

Intentia is not allowed to be unfalsifiable. Every strong interpretation must have a falsifier:

```text
interpretation: "urgency is distorting readiness"
falsifier: "both parties state calm explicit consent and urgency drops"
```
