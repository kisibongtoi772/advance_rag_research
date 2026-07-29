from typing import List
from rag_framework.core.interfaces import BaseGenerator, BaseEmbedding, Document
from rag_framework.providers.base_provider import BaseProvider
import random

class DummyGenerator(BaseGenerator):
    """A dummy generator that returns a mock response."""
    def generate(self, prompt: str, context: List[Document]) -> str:
        context_str = "\n".join([doc.content for doc in context])
        return f"Based on the context:\n{context_str}\n\nMock Answer: This is a simulated response to the prompt: {prompt}"

class DummyEmbedding(BaseEmbedding):
    """A dummy embedding model that returns random vectors (for testing)."""
    def __init__(self, dim: int = 1536):
        self.dim = dim

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[random.random() for _ in range(self.dim)] for _ in texts]

    def embed_query(self, query: str) -> List[float]:
        return [random.random() for _ in range(self.dim)]

class DummyProvider(BaseProvider):
    def get_generator(self) -> BaseGenerator:
        return DummyGenerator()
        
    def get_embedding(self) -> BaseEmbedding:
        return DummyEmbedding()
