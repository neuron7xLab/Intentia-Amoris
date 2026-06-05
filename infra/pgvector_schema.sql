-- Optional production optimization.
-- Current SQLAlchemy models store embeddings as JSON for SQLite portability.
-- In production, add a vector column and sync embeddings there.

CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE memory_chunks
  ADD COLUMN IF NOT EXISTS embedding_vec vector(384);

ALTER TABLE events
  ADD COLUMN IF NOT EXISTS embedding_vec vector(384);

CREATE INDEX IF NOT EXISTS idx_memory_chunks_embedding_vec
  ON memory_chunks USING ivfflat (embedding_vec vector_cosine_ops)
  WITH (lists = 100);
