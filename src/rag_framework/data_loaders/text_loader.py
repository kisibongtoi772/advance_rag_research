from typing import List
from rag_framework.core.interfaces import BaseDataLoader, Document

class TextLoader(BaseDataLoader):
    """A simple data loader for plain text files."""
    def load(self, source: str) -> List[Document]:
        # Implementation assumes 'source' is a filepath or string text.
        try:
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
            return [Document(content=content, metadata={"source": source})]
        except FileNotFoundError:
            # If not a file, treat source itself as the content
            return [Document(content=source, metadata={"source": "raw_text"})]
