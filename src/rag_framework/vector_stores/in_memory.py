from typing import List
from rag_framework.core.interfaces import BaseVectorStore, Document

class InMemoryVectorStore(BaseVectorStore):
    """A simple in-memory vector store that doesn't actually use vectors, just stores docs."""
    def __init__(self):
        self.documents: List[Document] = []

    def add_documents(self, documents: List[Document]) -> None:
        self.documents.extend(documents)

    def similarity_search(self, query: str, top_k: int = 4) -> List[Document]:
        # Naive implementation: just return first top_k docs for testing architecture
        return self.documents[:top_k]
