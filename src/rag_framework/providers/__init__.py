from rag_framework.providers.base_provider import BaseProvider
from rag_framework.providers.openai_provider import OpenAIProvider
from rag_framework.providers.anthropic_provider import AnthropicProvider
from rag_framework.providers.google_provider import GoogleProvider
from rag_framework.providers.deepseek_provider import DeepSeekProvider
from rag_framework.providers.qwen_provider import QwenProvider
from rag_framework.providers.dummy_provider import DummyProvider

class ProviderFactory:
    """Factory to retrieve the appropriate Provider based on a string name."""
    
    @staticmethod
    def create(provider_name: str) -> BaseProvider:
        name = provider_name.lower().strip()
        if name == "openai":
            return OpenAIProvider()
        elif name == "anthropic":
            return AnthropicProvider()
        elif name == "google" or name == "gemini":
            return GoogleProvider()
        elif name == "deepseek":
            return DeepSeekProvider()
        elif name == "qwen":
            return QwenProvider()
        elif name == "dummy":
            return DummyProvider()
        else:
            raise ValueError(f"Unknown LLM Provider: {provider_name}")
