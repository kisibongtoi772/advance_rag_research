import os
from typing import List
import dashscope
from http import HTTPStatus
from rag_framework.core.interfaces import BaseGenerator, BaseEmbedding, Document
from rag_framework.providers.base_provider import BaseProvider

class QwenGenerator(BaseGenerator):
    def __init__(self, model_name: str = "qwen-max"):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY not found.")
        dashscope.api_key = self.api_key
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
        
        response = dashscope.Generation.call(
            model=self.model_name,
            messages=[
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': user_message}
            ],
            result_format='message',
            temperature=0.0
        )
        
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0]['message']['content'].strip()
        else:
            raise RuntimeError(f"Qwen API error: {response.code} - {response.message}")

class QwenEmbedding(BaseEmbedding):
    def __init__(self, model_name: str = dashscope.TextEmbedding.Models.text_embedding_v2):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY not found.")
        dashscope.api_key = self.api_key
        self.model_name = model_name

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = dashscope.TextEmbedding.call(
            model=self.model_name,
            input=texts
        )
        if response.status_code == HTTPStatus.OK:
            return [res['embedding'] for res in response.output['embeddings']]
        else:
            raise RuntimeError(f"Qwen Embedding API error: {response.code} - {response.message}")

    def embed_query(self, query: str) -> List[float]:
        return self.embed_documents([query])[0]

class QwenProvider(BaseProvider):
    def get_generator(self) -> BaseGenerator:
        return QwenGenerator()
        
    def get_embedding(self) -> BaseEmbedding:
        return QwenEmbedding()
