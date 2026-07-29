from rag_framework.core.interfaces import BaseRetriever, BaseGenerator
from rag_framework.architectures.base import BaseRAGArchitecture

class BasicRAG(BaseRAGArchitecture):
    """
    Standard Vector Search RAG (Naive RAG).
    Flow: Retrieve -> Generate
    """
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self.retriever = retriever
        self.generator = generator

    def run(self, query: str) -> str:
        print("[BasicRAG] Retrieving context from vector store...")
        context = self.retriever.retrieve(query)
        
        print("[BasicRAG] Generating response based on retrieved context...")
        response = self.generator.generate(prompt=query, context=context)
        
        return response
