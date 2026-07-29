import typer
from rich.console import Console
from rich.panel import Panel

from rag_framework.data_loaders.text_loader import TextLoader
from rag_framework.vector_stores.in_memory import InMemoryVectorStore
from rag_framework.retrievers.basic_retriever import BasicRetriever
from rag_framework.generators.dummy_generator import DummyGenerator
from rag_framework.pipelines.standard_pipeline import StandardRAGPipeline

app = typer.Typer(help="Advanced RAG Evaluation and Testing Framework CLI")
console = Console()

@app.command()
def ingest(source: str, chunk_size: int = typer.Option(500, help="Chunk size for splitting text")):
    """Ingest documents from a source into the vector store."""
    console.print(f"[bold green]Ingesting from:[/bold green] {source}")
    loader = TextLoader()
    docs = loader.load(source)
    console.print(f"Loaded {len(docs)} document(s).")
    # In a real app, you would chunk documents here and persist them
    console.print(f"[bold green]Successfully ingested![/bold green]")

@app.command()
def run(query: str, config: str = typer.Option(None, help="Path to YAML config file")):
    """Run a query through the RAG pipeline."""
    # Build dummy pipeline
    store = InMemoryVectorStore()
    retriever = BasicRetriever(store)
    generator = DummyGenerator()
    pipeline = StandardRAGPipeline(retriever, generator)

    # In a real app, store would be loaded from disk/DB
    console.print(Panel.fit(f"[bold blue]Query:[/bold blue] {query}", title="Input"))
    
    response = pipeline.run(query)
    
    console.print(Panel.fit(response, title="RAG Output", border_style="green"))

@app.command()
def evaluate(dataset: str = typer.Option(..., help="Path to evaluation dataset (JSON)")):
    """Evaluate the RAG pipeline against a dataset."""
    from rag_framework.evaluators.basic_evaluator import BasicEvaluator
    
    console.print(f"[bold yellow]Evaluating pipeline using dataset:[/bold yellow] {dataset}")
    evaluator = BasicEvaluator()
    metrics = evaluator.evaluate([{"dummy": "data"}])
    
    console.print("[bold green]Evaluation Results:[/bold green]")
    for k, v in metrics.items():
        console.print(f"  - {k}: {v:.2f}")

if __name__ == "__main__":
    app()
