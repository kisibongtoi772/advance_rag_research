from rag_framework.core.interfaces import BaseGenerator, BaseRetriever, Document
from typing import List

class HydeRAG:
    """
    Hypothetical Document Embeddings (HyDE) Architecture.
    Uses the generator to create a hypothetical answer, then uses that answer to retrieve documents,
    and finally generates the real answer.
    """
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self.retriever = retriever
        self.generator = generator

    def run(self, query: str) -> str:
        # Step 1: Generate Hypothetical Document
        hypothetical_prompt = f"Please write a passage to answer the question: {query}"
        hypothetical_doc = self.generator.generate(hypothetical_prompt, context=[])
        
        # Step 2: Retrieve real documents using the hypothetical document as the query
        # In a strict HyDE implementation, the embedding model embeds hypothetical_doc directly.
        # Here we pass it to the retriever.
        retrieved_docs = self.retriever.retrieve(hypothetical_doc)
        
        # Step 3: Generate final answer
        final_answer = self.generator.generate(query, retrieved_docs)
        return final_answer
