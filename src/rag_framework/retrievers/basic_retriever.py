from typing import List
from rag_framework.core.interfaces import BaseRetriever, BaseVectorStore, Document

class BasicRetriever(BaseRetriever):
    """A standard retriever that wraps a vector store."""
    def __init__(self, vector_store: BaseVectorStore, top_k: int = 4):
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query: str) -> List[Document]:
        return self.vector_store.similarity_search(query, top_k=self.top_k)
