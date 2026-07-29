from rag_framework.core.interfaces import BaseRetriever, BaseGenerator
from rag_framework.architectures.base import BaseRAGArchitecture

class SelfRAG(BaseRAGArchitecture):
    """
    Self-Reflective RAG.
    Flow: Retrieve -> Generate -> Critique -> (Retry if failed) -> Final Output.
    """
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator, max_retries: int = 2):
        self.retriever = retriever
        self.generator = generator
        self.max_retries = max_retries

    def _critique(self, response: str) -> bool:
        """Simulate a critique step: checking if response is hallucinated or relevant."""
        # In a real scenario, this would call an LLM to grade the response.
        print("[SelfRAG] Critiquing the generated response...")
        return "Simulated" in response or "Mock" in response

    def run(self, query: str) -> str:
        attempts = 0
        while attempts <= self.max_retries:
            attempts += 1
            print(f"[SelfRAG] Attempt {attempts}/{self.max_retries + 1}: Retrieving context...")
            context = self.retriever.retrieve(query)
            
            print("[SelfRAG] Generating initial draft...")
            response = self.generator.generate(prompt=query, context=context)
            
            if self._critique(response):
                print("[SelfRAG] Response passed critique. Returning final answer.")
                return f"[Self-Corrected] {response}"
            else:
                print("[SelfRAG] Response failed critique. Retrying...")
                
        return "[SelfRAG] Failed to generate a reliable answer after max retries."
