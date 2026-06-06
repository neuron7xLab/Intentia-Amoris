# Risk Lattice

Verdict scope: repository genome snapshot, 2026-06-06.

## R1: state update path

Evidence -> `/events`, `/telemetry`, and `/media` read state, compute new scales, then write state in request handlers.
Mechanism -> parallel requests can compute from the same older row and overwrite each other.
Blast Radius -> canonical relationship state can stop matching the accepted event sequence.
Scale Trigger -> overlapping writes for the same pair id.
Probe -> concurrent mutation