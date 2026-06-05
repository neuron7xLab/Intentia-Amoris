# Intentia Amoris — Production Roadmap

**Document class:** engineering roadmap  
**Target:** production-grade local-first intelligence system  
**Mode:** privacy-first | consent-first | evidence-first | local-first | research-grade | product-ready

---

## 1. Canonical Product Target

Intentia Amoris must become a verified system, not a narrative artifact.

The product target is:

```text
bounded memory + consent gate + local encryption + hybrid retrieval + eval harness + audit ledger
```

A feature is accepted only when it has tests, deterministic evidence, clear boundaries, and a reproducible command.

---

## 2. Maturity Ladder

### L0 — Repository Scaffold

- README explains product thesis.
- Core boundaries are documented.
- Local start command exists.
- Basic tests exist.

### L1 — Deterministic Event Layer

- Input events normalize into stable JSONL.
- Each event has timestamp, source class, hash, and schema version.
- Parser output is reproducible.
- Evidence inventory is generated.

### L2 — Consent-Gated Retrieval

- Consent ledger exists.
- Vector retrieval accepts consent filters.
- Graph traversal accepts consent filters.
- Revoked streams are excluded from inference.
- Runtime emits masked-context audit records.

### L3 — Local-First Privacy

- Field-level encryption works locally.
- Nonce uniqueness is tested.
- Plaintext is not persisted in generated artifacts.
- Sync payloads remain ciphertext.
- Key handling has test coverage.

### L4 — Eval-Gated Synthesis

- Every answer maps claims to evidence classes.
- Unsupported claims become UNKNOWN.
- Unsafe or unsupported output is blocked.
- Attestation JSON is emitted for each synthesis.

### L5 — Research-Grade Evidence

- Experiments have explicit hypotheses.
- Metrics and failure modes are declared.
- Negative controls exist.
- Reproducibility commands are documented.
- Release gate checks evidence bundles.

### L6 — Public Canonical Artifact

- Synthetic demo exists.
- Architecture paper exists.
- Security model exists.
- Product page exists.
- CI evidence is reproducible from a clean checkout.

---

## 3. RIOS-001: First Production Slice

Goal:

```text
prove that unauthorized context cannot enter retrieval or synthesis
```

Required files:

```text
src/intentia/consent/ledger.py
src/intentia/consent/mask.py
src/intentia/memory/retrieval_contract.py
src/intentia/evals/attestation.py
tests/test_consent_masking.py
tests/test_revocation_blocks_retrieval.py
tests/test_attestation_contract.py
evidence/RIOS_001/attestation.json
```

Acceptance command:

```bash
pytest -q
python -m compileall -q src
```

Release gate:

```yaml
riOS_001_gate:
  tests_pass: true
  no_skip_or_xfail: true
  consent_masking_pass: true
  revocation_pass: true
  unsupported_claims_become_unknown: true
  deterministic_attestation_json: true
```

---

## 4. Canonical Runtime Flow

```text
input
  -> schema validation
  -> local protection boundary
  -> consent gate
  -> event-source append
  -> vector projection
  -> graph projection
  -> hybrid retrieval
  -> eval harness
  -> bounded synthesis
  -> audit ledger
```

Forbidden shortcut:

```text
input -> prompt -> confident answer
```

That shortcut is how prototypes become expensive confetti.

---

## 5. Engineering Rule

Nothing is promoted from idea to product unless it creates a verifiable artifact:

```text
spec -> code -> test -> evidence -> release gate -> documented boundary
```

If one link is missing, the claim remains experimental.
