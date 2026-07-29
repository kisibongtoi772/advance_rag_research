import os
from typing import List
from openai import OpenAI
from rag_framework.core.interfaces import BaseGenerator, BaseEmbedding, Document
from rag_framework.providers.base_provider import BaseProvider

class OpenAIGenerator(BaseGenerator):
    def __init__(self, model_name: str = "gpt-4o"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found.")
        self.client = OpenAI(api_key=self.api_key)
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
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "system", "content": system_message}, {"role": "user", "content": user_message}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()

class OpenAIEmbedding(BaseEmbedding):
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found.")
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = model_name

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(input=texts, model=self.model_name)
        return [data.embedding for data in response.data]

    def embed_query(self, query: str) -> List[float]:
        response = self.client.embeddings.create(input=[query], model=self.model_name)
        return response.data[0].embedding

class OpenAIProvider(BaseProvider):
    def get_generator(self) -> BaseGenerator:
        return OpenAIGenerator()
        
    def get_embedding(self) -> BaseEmbedding:
        return OpenAIEmbedding()
