# Risk Lattice

R1 state: E->api read/compute/write. M->stale row overwrite. B->state drift. S->same-pair burst. P->parallel events. F->state service.

R2 retrieval: E->Python sort of chunks. M->linear scan. B->latency wall. S->large memory table. P->100k fixture. F->SQL vector search.

R3 media: E->file.read. M->full upload in RAM. B->RSS spike. S->parallel uploads. P->15MiB flood. F->stream chunks.

R4 embed: E->new AsyncOpenAI per call. M->no pool. B->network stall. S->remote provider mode. P->timeout sim. F->pooled client.

R5 audit: E->local jsonl chain. M->local append. B->ledger fork. S->multi worker. P->parallel append. F->db sink.

R6 import: E->whole-file