import os
from typing import List
from anthropic import Anthropic
from rag_framework.core.interfaces import BaseGenerator, BaseEmbedding, Document
from rag_framework.providers.base_provider import BaseProvider

class AnthropicGenerator(BaseGenerator):
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found.")
        self.client = Anthropic(api_key=self.api_key)
        self.model_name = model_name

    def generate(self, prompt: str, context: List[Document]) -> str:
        context_str = "\n".join([f"Document {i+1}: {doc.content}" for i, doc in enumerate(context)])
        system_message = (
            "You are an expert AI assistant utilized within an enterprise RAG system. "
            "Your objective is to answer the user's query strictly based on the provided context documents. "
            "If the information is not present in the context, explicitly state that the information is unavailable. "
            "Do not hallucinate."
        )
        user_message = f"Context Documents:\n{context_str}\n\nQuery: {prompt}"
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=1024,
            system=system_message,
            messages=[{"role": "user", "content": user_message}],
            temperature=0.0
        )
        return response.content[0].text.strip()

class AnthropicEmbedding(BaseEmbedding):
    def __init__(self):
        # Anthropic doesn't have a public embedding model yet, so we use VoyageAI or OpenAI.
        # For simplicity in this framework, we'll fall back to OpenAI for embeddings 
        # when using Claude, or we can use a dummy if strict isolation is needed.
        # We will use OpenAI for embeddings here since Voyage API isn't explicitly configured.
        from openai import OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found (Required for Anthropic Embeddings fallback).")
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = "text-embedding-3-small"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(input=texts, model=self.model_name)
        return [data.embedding for data in response.data]

    def embed_query(self, query: str) -> List[float]:
        response = self.client.embeddings.create(input=[query], model=self.model_name)
        return response.data[0].embedding

class AnthropicProvider(BaseProvider):
    def get_generator(self) -> BaseGenerator:
        return AnthropicGenerator()
        
    def get_embedding(self) -> BaseEmbedding:
        return AnthropicEmbedding()
