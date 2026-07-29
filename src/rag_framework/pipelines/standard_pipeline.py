from rag_framework.core.interfaces import BaseRetriever, BaseGenerator

class StandardRAGPipeline:
    """End-to-end RAG pipeline tying retriever and generator together."""
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self.retriever = retriever
        self.generator = generator

    def run(self, query: str) -> str:
        context = self.retriever.retrieve(query)
        response = self.generator.generate(prompt=query, context=context)
        return response
