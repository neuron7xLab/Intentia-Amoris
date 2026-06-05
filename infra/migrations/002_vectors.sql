-- pgvector target schema for future production retrieval.
-- Current Python code stores embeddings as JSON for SQLite compatibility.
-- When moving fully to Postgres, add vector columns and approximate indexes.

-- ALTER TABLE events ADD COLUMN embedding_vec vector(384);
-- CREATE INDEX IF NOT EXISTS idx_events_embedding_hnsw ON events USING hnsw (embedding_vec vector_cosine_ops);
