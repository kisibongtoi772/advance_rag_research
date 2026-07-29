from rag_framework.core.interfaces import BaseGenerator, BaseRetriever, Document
from typing import List

class SelfAskRAG:
    """
    Self-Ask Prompting Architecture.
    Breaks down a complex user query into sub-questions, retrieves context for each, 
    and synthesizes a final answer.
    """
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self.retriever = retriever
        self.generator = generator

    def run(self, query: str) -> str:
        # Step 1: Generate sub-questions
        breakdown_prompt = (
            f"Given the complex question: '{query}', break it down into 2 simpler sub-questions "
            "that need to be answered first. Only output the sub-questions, one per line."
        )
        sub_questions_raw = self.generator.generate(breakdown_prompt, context=[])
        sub_questions = [sq.strip() for sq in sub_questions_raw.split('\n') if sq.strip()]
        
        # Step 2: Retrieve and answer sub-questions (The Scratchpad)
        scratchpad = ""
        for sq in sub_questions:
            docs = self.retriever.retrieve(sq)
            sq_answer = self.generator.generate(f"Answer this sub-question briefly: {sq}", context=docs)
            scratchpad += f"Sub-question: {sq}\nIntermediate Answer: {sq_answer}\n\n"
            
        # Step 3: Final Synthesis
        synthesis_prompt = (
            f"Using the following intermediate findings, answer the original question.\n\n"
            f"Original Question: {query}\n\nFindings:\n{scratchpad}"
        )
        # We pass an empty context here because the context is already synthesized into the prompt
        final_answer = self.generator.generate(synthesis_prompt, context=[])
        
        return final_answer
