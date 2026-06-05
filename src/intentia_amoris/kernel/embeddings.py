from __future__ import annotations

import hashlib
import math
import re
from abc import ABC, abstractmethod

import numpy as np

from intentia_amoris.config import get_settings


class EmbeddingProvider(ABC):
    dim: int

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        raise NotImplementedError


class LocalHashEmbeddingProvider(EmbeddingProvider):
    """
    Fast deterministic feature-hashing embeddings.

    This is not semantic like a neural embedding model, but it gives:
    - stable vectors;
    - no external dependency;
    - fast tests;
    - production-safe fallback.
    """

    def __init__(self, dim: int = 384) -> None:
        self.dim = dim

    async def embed(self, text: str) -> list[float]:
        return self.embed_sync(text)

    def embed_sync(self, text: str) -> list[float]:
        vec = np.zeros(self.dim, dtype=np.float32)
        tokens = re.findall(r"[\wʼ'’\-]+", text.lower(), flags=re.UNICODE)
        if not tokens:
            return vec.tolist()

        for token in tokens:
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            idx = int.from_bytes(digest[:4], "little") % self.dim
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            weight = 1.0 + min(len(token), 12) / 24.0
            vec[idx] += sign * weight

        norm = float(np.linalg.norm(vec))
        if norm > 0:
            vec /= norm
        return vec.tolist()


class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model: str, dim: int) -> None:
        self.model = model
        self.dim = dim

    async def embed(self, text: str) -> list[float]:
        from openai import AsyncOpenAI

        settings = get_settings()
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        resp = await client.embeddings.create(model=self.model, input=text)
        vec = resp.data[0].embedding
        if len(vec) != self.dim:
            # Keep schema stable. Truncate or pad by config.
            if len(vec) > self.dim:
                vec = vec[: self.dim]
            else:
                vec = vec + [0.0] * (self.dim - len(vec))
        return vec


def cosine(a: list[float] | np.ndarray, b: list[float] | np.ndarray) -> float:
    aa = np.asarray(a, dtype=np.float32)
    bb = np.asarray(b, dtype=np.float32)
    denom = float(np.linalg.norm(aa) * np.linalg.norm(bb))
    if denom == 0:
        return 0.0
    return float(np.dot(aa, bb) / denom)


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def get_embedding_provider() -> EmbeddingProvider:
    settings = get_settings()
    if settings.embedding_provider == "openai" and settings.openai_api_key:
        return OpenAIEmbeddingProvider(settings.openai_embedding_model, settings.embedding_dim)
    return LocalHashEmbeddingProvider(settings.embedding_dim)
