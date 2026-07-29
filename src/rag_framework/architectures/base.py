from abc import ABC, abstractmethod

class BaseRAGArchitecture(ABC):
    """Base class for all RAG architectures."""
    
    @abstractmethod
    def run(self, query: str) -> str:
        """Executes the RAG pipeline for the given query and returns the answer."""
        pass
