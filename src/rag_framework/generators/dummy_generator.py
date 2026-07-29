from typing import List
from rag_framework.core.interfaces import BaseGenerator, Document

class DummyGenerator(BaseGenerator):
    """A dummy generator that returns a mock response."""
    def generate(self, prompt: str, context: List[Document]) -> str:
        context_str = "\n".join([doc.content for doc in context])
        return f"Based on the context:\n{context_str}\n\nMock Answer: This is a simulated response to the prompt: {prompt}"
