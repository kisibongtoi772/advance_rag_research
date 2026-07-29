from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class Document(BaseModel):
    """Core domain model representing a chunk of text or multimodal data."""
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    doc_id: Optional[str] = None
    image_base64: Optional[str] = None  # For Multimodal RAG

class GraphNode(BaseModel):
    """Represents a node (entity) in Graph RAG."""
    node_id: str
    label: str
    properties: Dict[str, Any] = Field(default_factory=dict)

class GraphEdge(BaseModel):
    """Represents an edge (relationship) in Graph RAG."""
    source_id: str
    target_id: str
    relationship: str
    weight: float = 1.0

class BaseDataLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> List[Document]:
        """Loads documents from a specific source."""
        pass

class BaseEmbedding(ABC):
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embeds a list of documents."""
        pass

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embeds a single query."""
        pass

class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> None:
        """Adds documents to the vector store."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, top_k: int = 4) -> List[Document]:
        """Searches for similar documents based on the query."""
        pass

class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> List[Document]:
        """Retrieves relevant documents for a query."""
        pass

class BaseGenerator(ABC):
    @abstractmethod
    def generate(self, prompt: str, context: List[Document]) -> str:
        """Generates a response given a prompt and retrieved context."""
        pass

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, dataset: List[Dict[str, Any]]) -> Dict[str, float]:
        """Evaluates the pipeline on a given dataset and returns metrics."""
        pass
