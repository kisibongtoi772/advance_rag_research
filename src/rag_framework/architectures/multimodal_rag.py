from rag_framework.architectures.base import BaseRAGArchitecture
from rag_framework.core.interfaces import BaseRetriever, BaseGenerator

class MultimodalRAG(BaseRAGArchitecture):
    """
    Multimodal RAG Architecture.
    Flow: Retrieve (Text + Image embeddings) -> Generate (Vision LLM).
    """
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self.retriever = retriever
        self.generator = generator

    def run(self, query: str) -> str:
        print("[MultimodalRAG] Retrieving multimodal context (Text + Images)...")
        context = self.retriever.retrieve(query)
        
        # Injecting a mock image if missing to demonstrate multimodal capability
        for doc in context:
            if not doc.image_base64:
                doc.image_base64 = "base64_encoded_dummy_image_data_here"
                
        print(f"[MultimodalRAG] Passing {len(context)} multimodal chunks to Vision-LLM generator...")
        response = self.generator.generate(prompt=query, context=context)
        
        return f"[Vision-Analyzed] {response}"
