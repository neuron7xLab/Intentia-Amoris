# Intentia Amoris OS v2026.4 — Execution State

**Status:** initialized specification layer  
**Repository:** `neuron7xLab/Intentia-Amoris`  
**Mode:** privacy-first | consent-first | evidence-first | local-first | research-grade | product-ready  
**Primary boundary:** relationship intelligence infrastructure, not therapy, not mind-reading, not coercion, not a substitute for living consent.

---

## 0. Canonical Operating Thesis

Intentia Amoris OS is a local-first Relationship Intelligence Operating System for bounded, consent-gated, evidence-grounded interpretation of relational events.

The system may compute:

```text
facts + memory + body + consent + inference + time
  -> bounded relational state
  -> safer question
  -> safer repair protocol
  -> audit trail
```

The system must not compute:

```text
pressure
surveillance
coercion
diagnosis without clinician authority
hormonal claims without measured data
partner intent without evidence
consent by inference
```

---

## 1. Hard Invariants

### I1. Consent is a computation gate

No event, telemetry stream, message, media object, or derived inference may be used unless the current consent ledger authorizes its use for the active inference scope.

```python
if not consent.permits(subject, stream, purpose, recipient):
    mask(stream)
    suppress_edges(stream)
    deny_explanation(stream)
```

### I2. Privacy treats cloud as compromised

All private relational payloads are toxic assets unless locally encrypted before persistence or synchronization.

Required state:

```text
plaintext lifetime <= active local process window
at-rest payloads = encrypted
sync payloads = encrypted
server visibility = metadata-minimized
```

### I3. No evidence, no claim

Every output claim must map to one of:

```text
HARD_TELEMETRY
SUBJECTIVE_TELEMETRY
EVENT_LOG
CONSENT_LEDGER
DERIVED_INFERENCE
UNKNOWN
```

If the backing source is missing, the system must emit `UNKNOWN`, not narrative improvisation. Humanity keeps inventing romance and then acting shocked when ambiguity explodes. The machine will not help with that.

### I4. Safety dominates optimization

If abuse, coercion, fear, stalking, self-harm, severe destabilization, or loss of autonomy is detected, the system enters safety mode.

```text
relationship_optimization = disabled
persuasion_generation = disabled
repair_protocol = safety-first
recommendation = pause / boundary / external support / emergency escalation when appropriate
```

### I5. Living persons dominate digital twins

Any partner may revoke, delete, mask, export, or disable their own data. Revocation invalidates future inference over the revoked stream.

---

## 2. Evidence Taxonomy

| Class | Definition | Examples | Allowed Inference |
|---|---|---|---|
| `HARD_TELEMETRY` | Objective device or lab-derived data | HRV, sleep duration, steps, verified lab cortisol | capacity estimate, fatigue risk, timing caution |
| `SUBJECTIVE_TELEMETRY` | Self-report | mood, journal, perceived conflict intensity | self-stated emotional state only |
| `EVENT_LOG` | Timestamped interaction evidence | messages, calls, reactions, repair attempts | sequence, recurrence, escalation/repair pattern |
| `CONSENT_LEDGER` | Explicit access scope | telemetry permission, sharing revocation | mask/allow inference scope |
| `DERIVED_INFERENCE` | Computed latent state | reactivity risk, repair window estimate | probabilistic, bounded, never treated as fact |
| `UNKNOWN` | Missing or unauthorized data | no consent, no telemetry, corrupted source | no claim |

---

## 3. Data Model

### 3.1 Event envelope

```json
{
  "event_id": "uuid-v7-or-content-hash",
  "occurred_at": "2026-06-05T00:00:00Z",
  "ingested_at": "2026-06-05T00:00:01Z",
  "subject_id": "partner_alpha|partner_beta|dyad",
  "stream": "message|call|media|hrv|sleep|journal|consent|repair",
  "evidence_class": "EVENT_LOG",
  "payload_ref": "encrypted://local/blob/hash",
  "consent_scope_ref": "consent://ledger/version",
  "source_integrity": {
    "sha256": "...",
    "signature": "optional",
    "parser_version": "intentia-ingest-v1"
  }
}
```

### 3.2 Consent record

```json
{
  "consent_id": "uuid-v7",
  "subject_id": "partner_alpha",
  "recipient_id": "partner_beta|system|research_export",
  "stream": "hrv|sleep|messages|media|journal",
  "purpose": "repair|state_summary|research|product_eval",
  "access_level": "none|aggregate|gradient|full",
  "expires_at": "nullable",
  "revoked_at": "nullable",
  "created_at": "2026-06-05T00:00:00Z",
  "signature": "local-passkey-signature"
}
```

### 3.3 Graph schema

```text
(:Partner {id})
(:Event {id, occurred_at, evidence_class})
(:Emotion {label, intensity_source})
(:ConflictTrigger {label})
(:RepairAttempt {type, outcome})
(:TelemetryWindow {stream, started_at, ended_at})
(:ConsentScope {id, stream, purpose, access_level})
```

Edges:

```text
(:Partner)-[:AUTHORIZES]->(:ConsentScope)
(:Event)-[:HAS_EVIDENCE]->(:ConsentScope)
(:TelemetryWindow)-[:AFFECTS {weight, confidence}]->(:Event)
(:Event)-[:TRIGGERS {weight, evidence_ref}]->(:Emotion)
(:Event)-[:ESCALATES {weight}]->(:ConflictTrigger)
(:RepairAttempt)-[:REPAIRS {confidence, evidence_ref}]->(:Event)
```

---

## 4. Hybrid Retrieval Contract

Every inference must combine semantic retrieval and structural retrieval.

```text
candidate_context =
  KNN_vector(query_embedding, k=12, filter=consent_scope)
  UNION
  BFS_graph(anchor_entities, depth=2, filter=consent_scope)
```

### Required masking

```python
for node_or_edge in candidate_context:
    if not consent_ledger.authorizes(node_or_edge):
        candidate_context.remove(node_or_edge)
        audit.log("CONSENT_MASKED", node_or_edge.redacted_ref)
```

### Retrieval output schema

```json
{
  "query_id": "uuid-v7",
  "vector_hits": [
    {
      "chunk_id": "...",
      "similarity": 0.87,
      "evidence_class": "EVENT_LOG",
      "consent_status": "authorized"
    }
  ],
  "graph_paths": [
    {
      "path": ["Partner", "Event", "Emotion"],
      "depth": 2,
      "confidence": 0.74,
      "evidence_refs": ["event://..."]
    }
  ],
  "masked_items_count": 0
}
```

---

## 5. Local-First Encryption Contract

### Required primitive

```text
AES-256-GCM
unique nonce per encryption operation
associated data = schema_version + stream + subject_id + consent_scope_id
key material = local passkey / passphrase-derived key
```

### Forbidden states

```text
reused nonce with same key
plaintext telemetry in cloud logs
unencrypted dialogue exports in remote object storage
server-side-only consent enforcement
hardcoded production secrets
```

### Verification target

```text
unit: encrypt/decrypt roundtrip
unit: tamper detection fails closed
unit: nonce uniqueness over N operations
unit: revoked stream cannot decrypt for inference path
integration: sync payload remains ciphertext outside local boundary
```

Current attestation status:

```yaml
encryption_layer_verification: REQUIRED_NOT_YET_REVALIDATED_BY_THIS_SPEC
```

---

## 6. Clinical Safety Boundary

The system may generate:

```text
reflection prompts
pause protocols
repair scripts
consent checks
capacity-aware timing suggestions
non-diagnostic risk summaries
```

The system must refuse or hard-stop:

```text
manipulation tactics
gaslighting scripts
jealousy amplification
surveillance instructions
pressure after refusal
threats or coercion
psychological diagnosis as fact
medical interpretation without clinician-grade evidence
```

### Safety mode trigger

```json
{
  "trigger_type": "coercion|abuse|self_harm|destabilization|consent_violation",
  "severity": "low|medium|high|critical",
  "action": "mask|pause|boundary|external_support|emergency_guidance",
  "relationship_advice_enabled": false
}
```

---

## 7. Eval Harness

No generated relational output is valid until it passes these checks.

| Gate | Requirement | Fail behavior |
|---|---:|---|
| Consent scope | 100% authorized context | mask unauthorized data |
| Non-coercion | 100% pass | refuse and rewrite safely |
| Evidence mapping | every claim has source class | downgrade to `UNKNOWN` |
| Context accuracy | no invented dates/events | block output |
| Clinical boundary | no diagnosis/therapy replacement | rewrite as support protocol |
| Privacy | no plaintext secret/private payload leakage | block output |

### Attestation schema

```yaml
eval_harness_attestation:
  consent_scope_pass: true
  non_coercion_pass: true
  evidence_mapping_pass: true
  contextual_accuracy_pass: true
  clinical_boundary_pass: true
  privacy_leakage_pass: true
  hallucination_index: 0.00
  blocked_claims: []
  masked_context_items: 0
```

The numbers are valid only if produced by implemented tests or runtime checks. Otherwise they remain target metrics, not evidence. Because apparently this has to be said in 2026.

---

## 8. Runtime Output Schema

### 8.1 Input Telemetry Ingestion Ledger

```json
{
  "telemetry_source": "Apple_HealthKit|Google_Fit|manual|none",
  "partner_alpha": {
    "hrv_delta_ms": null,
    "sleep_efficiency_pct": null,
    "step_count": null,
    "source_status": "unknown"
  },
  "partner_beta": {
    "hrv_delta_ms": null,
    "sleep_efficiency_pct": null,
    "step_count": null,
    "source_status": "unknown"
  },
  "consent_status": {
    "alpha_to_beta": "unknown|none|aggregate|gradient|full",
    "beta_to_alpha": "unknown|none|aggregate|gradient|full"
  }
}
```

### 8.2 Cognitive Memory Retrieval Graph Linkage

```json
{
  "vector_subsystem": {
    "enabled": true,
    "backend": "pgvector|local-faiss|unknown",
    "authorized_hits": [],
    "masked_hits": []
  },
  "graph_subsystem": {
    "enabled": true,
    "backend": "kuzu|neo4j|unknown",
    "authorized_paths": [],
    "masked_paths": []
  }
}
```

### 8.3 Production-Ready Clinical Synthesis

```json
{
  "current_relational_vector": {
    "status": "UNKNOWN_UNTIL_RETRIEVAL",
    "confidence": 0.0,
    "evidence_refs": []
  },
  "micro_intervention": {
    "type": "pause|repair|question|boundary|external_support",
    "steps": [],
    "contraindications": []
  }
}
```

### 8.4 Guardrail Verification Attestation

```yaml
eval_harness_attestation:
  consent_scope_pass: null
  non_coercion_pass: null
  evidence_mapping_pass: null
  contextual_accuracy_pass: null
  clinical_boundary_pass: null
  privacy_leakage_pass: null
  hallucination_index: null
  encryption_layer_verification: REQUIRED_NOT_YET_REVALIDATED_BY_THIS_SPEC
  safety_interlock_status: INITIALIZED_NOT_EXECUTED
```

---

## 9. Product Acceptance Criteria

### P0: Trust boundary

- No private plaintext persisted outside local trusted boundary.
- Consent ledger exists and gates retrieval.
- Revocation invalidates future inference.
- Safety hard-stop exists.
- Every answer has evidence mapping.

### P1: Memory engine

- Event-source ingestion normalizes dialogue, media, calls, repairs, conflict markers.
- Vector memory supports consent-filtered semantic retrieval.
- Graph memory supports consent-filtered causal/topological traversal.
- Audit trail records masked context and blocked claims.

### P2: Relationship intelligence loop

- System outputs safer questions before advice when evidence is incomplete.
- System prefers de-escalation over persuasion.
- System tracks repair attempts and outcomes.
- System never optimizes engagement at the cost of autonomy.

### P3: Research-grade verification

- Deterministic eval fixtures.
- Adversarial manipulation tests.
- Consent masking tests.
- Encryption misuse tests.
- Regression suite for hallucinated partner-intent claims.

---

## 10. Initial Execution State

```yaml
intentia_amoris_os:
  version: "2026.4"
  initialized_at: "2026-06-05"
  operating_mode:
    - privacy_first
    - consent_first
    - evidence_first
    - local_first
    - research_grade
    - product_ready
  state:
    specification_layer: initialized
    repository_binding: neuron7xLab/Intentia-Amoris
    runtime_validation: pending
    ci_validation: pending
    encryption_revalidation: pending
    consent_gate_revalidation: pending
    eval_harness_revalidation: pending
  hard_boundary:
    therapy_replacement: false
    mind_reading: false
    coercion: false
    inferred_consent: false
    hormone_claims_without_lab_data: false
```

---

## 11. Next Implementation Slice

The next concrete engineering slice must be small and falsifiable:

```text
Slice RIOS-001:
  1. implement/verify consent-filtered retrieval contract
  2. add tests for unauthorized telemetry masking
  3. add tests for revoked consent invalidating graph edges
  4. add eval fixture that blocks coercive/gaslighting outputs
  5. emit guardrail attestation JSON from runtime path
```

Done means:

```text
pytest passes
no skip/xfail
no plaintext private payload in generated artifacts
all relational outputs include evidence_class mapping
unauthorized streams are absent from vector and graph retrieval results
```
