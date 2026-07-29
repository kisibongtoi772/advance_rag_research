import os
from typing import List
import google.generativeai as genai
from rag_framework.core.interfaces import BaseGenerator, BaseEmbedding, Document
from rag_framework.providers.base_provider import BaseProvider

class GoogleGenerator(BaseGenerator):
    def __init__(self, model_name: str = "gemini-1.5-pro-latest"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found.")
        genai.configure(api_key=self.api_key)
        
        system_message = (
            "You are an expert AI assistant utilized within an enterprise RAG system. "
            "Your objective is to answer the user's query strictly based on the provided context documents. "
            "If the information is not present in the context, explicitly state that the information is unavailable. "
            "Do not hallucinate."
        )
        self.model = genai.GenerativeModel(model_name, system_instruction=system_message)

    def generate(self, prompt: str, context: List[Document]) -> str:
        context_str = "\n".join([f"Document {i+1}: {doc.content}" for i, doc in enumerate(context)])
        user_message = f"Context Documents:\n{context_str}\n\nQuery: {prompt}"
        
        response = self.model.generate_content(
            user_message,
            generation_config=genai.GenerationConfig(temperature=0.0)
        )
        return response.text.strip()

class GoogleEmbedding(BaseEmbedding):
    def __init__(self, model_name: str = "models/text-embedding-004"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found.")
        genai.configure(api_key=self.api_key)
        self.model_name = model_name

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = genai.embed_content(
            model=self.model_name,
            content=texts,
            task_type="retrieval_document"
        )
        return response['embedding']

    def embed_query(self, query: str) -> List[float]:
        response = genai.embed_content(
            model=self.model_name,
            content=query,
            task_type="retrieval_query"
        )
        return response['embedding']

class GoogleProvider(BaseProvider):
    def get_generator(self) -> BaseGenerator:
        return GoogleGenerator()
        
    def get_embedding(self) -> BaseEmbedding:
        return GoogleEmbedding()
