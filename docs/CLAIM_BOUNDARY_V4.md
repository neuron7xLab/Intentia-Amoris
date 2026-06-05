# Claim Boundary v4

## Valid claims

Intentia may claim:

- a message exists in the event log
- a media artifact exists in the manifest
- a participant self-reported a state
- a telemetry device submitted a metric
- a lab result was provided
- a model inferred a pattern with uncertainty
- a value function produced a score from defined inputs

## Invalid claims

Intentia may not claim:

- Dasha feels X without Dasha's own signal
- Yaroslav's hormones are X without lab data
- the model knows the true meaning of a photo
- a future commitment exists because past messages were intimate
- the avatar is the person
- intensity equals love
- jealousy equals proof
- desire equals consent

## Required labels

Every generated conclusion must be one of:

```text
OBSERVED
SELF_REPORTED
PARTNER_REPORTED
MEASURED
RETRIEVED
INFERRED
UNKNOWN
```
