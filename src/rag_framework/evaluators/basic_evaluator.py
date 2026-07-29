from typing import List, Dict, Any
from rag_framework.core.interfaces import BaseEvaluator

class BasicEvaluator(BaseEvaluator):
    """A basic evaluator that mocks the evaluation process."""
    def evaluate(self, dataset: List[Dict[str, Any]]) -> Dict[str, float]:
        # Simulating evaluation metrics like those from Ragas
        return {
            "context_precision": 0.85,
            "context_recall": 0.90,
            "answer_relevancy": 0.88,
            "faithfulness": 0.92
        }
