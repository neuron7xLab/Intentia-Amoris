# Risk Lattice

R1 state: Evidence -> API routes read/compute/write state. Mechanism -> concurrent writers use stale rows. Blast Radius -> state diverges from event log. Scale Trigger -> overlapping writes per pair. Probe -> concurrent event test. Minimal Fix -> state mutation service with row lock/version.

R2 retrieval: Evidence -> search_memory loads chunks then Python-sorts. Mechanism -> O(N log N) request