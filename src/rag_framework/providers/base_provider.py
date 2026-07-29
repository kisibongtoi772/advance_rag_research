from abc import ABC, abstractmethod
from rag_framework.core.interfaces import BaseGenerator, BaseEmbedding

class BaseProvider(ABC):
    """Abstract factory for creating provider-specific Generators and Embeddings."""
    
    @abstractmethod
    def get_generator(self) -> BaseGenerator:
        pass
        
    @abstractmethod
    def get_embedding(self) -> BaseEmbedding:
        pass
