# Risk Lattice

R1 state: E->api r/c/w. M->stale row. B->state drift. S->pair burst. P->parallel events. F->state service.

R2 retrieval: E->Python sort. M->linear scan. B->latency wall. S->many chunks. P->100k fixture. F->SQL vector.

R3 media: E->file.read. M->full RAM. B->RSS spike. S->parallel upload. P->15MiB flood. F->stream chunks.

R4 embed: E->new client. M->no pool. B->stall. S->remote mode. P->timeout sim. F->pooled client.

R5 audit: E->jsonl chain.