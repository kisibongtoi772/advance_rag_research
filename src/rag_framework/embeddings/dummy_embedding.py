from typing import List
import random
from rag_framework.core.interfaces import BaseEmbedding

class DummyEmbedding(BaseEmbedding):
    """A dummy embedding model that returns random vectors (for testing)."""
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[random.random() for _ in range(self.dimension)] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return [random.random() for _ in range(self.dimension)]
