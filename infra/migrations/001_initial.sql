-- Intentia Amoris initial schema notes.
-- Runtime models are created by SQLAlchemy in dev/test.
-- Production can either use Alembic later or load these contracts manually.

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
