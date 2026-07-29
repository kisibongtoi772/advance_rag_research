import os
from typing import List
from openai import OpenAI
from rag_framework.core.interfaces import BaseGenerator, BaseEmbedding, Document
from rag_framework.providers.base_provider import BaseProvider

class DeepSeekGenerator(BaseGenerator):
    def __init__(self, model_name: str = "deepseek-chat"):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found.")
        # DeepSeek is OpenAI-compatible
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")
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

class DeepSeekEmbedding(BaseEmbedding):
    def __init__(self):
        # DeepSeek doesn't offer a public standalone embedding API matching OpenAI perfectly yet in standard use, 
        # or it does via specific endpoints. 
        # For this framework, we'll use OpenAI for embeddings if a DeepSeek embedding model isn't configured,
        # or we attempt to use deepseek's model if they added it (e.g., deepseek-embed).
        # We will use OpenAI here as a fallback to ensure robustness for RAG.
        from openai import OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found (Required for DeepSeek Embeddings fallback).")
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = "text-embedding-3-small"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(input=texts, model=self.model_name)
        return [data.embedding for data in response.data]

    def embed_query(self, query: str) -> List[float]:
        response = self.client.embeddings.create(input=[query], model=self.model_name)
        return response.data[0].embedding

class DeepSeekProvider(BaseProvider):
    def get_generator(self) -> BaseGenerator:
        return DeepSeekGenerator()
        
    def get_embedding(self) -> BaseEmbedding:
        return DeepSeekEmbedding()
