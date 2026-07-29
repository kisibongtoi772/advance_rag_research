from rag_framework.core.interfaces import BaseGenerator, BaseRetriever, Document
from typing import List

class CorrectiveRAG:
    """
    Corrective Retrieval Augmented Generation (CRAG).
    Evaluates the quality of retrieved documents before generation. 
    If documents are deemed irrelevant, it rewrites the query and retries retrieval.
    """
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self.retriever = retriever
        self.generator = generator

    def run(self, query: str) -> str:
        # Step 1: Initial Retrieval
        docs = self.retriever.retrieve(query)
        
        # Step 2: Lightweight Retrieval Evaluation
        context_str = "\n".join([doc.content for doc in docs])
        eval_prompt = (
            f"You are a retrieval evaluator. Given the user query '{query}', do the following documents "
            f"contain sufficient information to answer it? Reply with exactly 'YES' or 'NO'.\n\nDocuments:\n{context_str}"
        )
        
        # Assuming the generator can handle this classification task
        eval_result = self.generator.generate(eval_prompt, context=[])
        
        # Step 3: Corrective Loop
        if "YES" not in eval_result.upper():
            # Rewrite the query for better semantic matching
            rewrite_prompt = (
                f"The original query '{query}' returned poor search results. "
                f"Rewrite it into a more precise search query. Return ONLY the rewritten query."
            )
            new_query = self.generator.generate(rewrite_prompt, context=[])
            
            # Secondary retrieval with rewritten query
            docs = self.retriever.retrieve(new_query)
            
        # Step 4: Final Generation
        return self.generator.generate(query, context=docs)
