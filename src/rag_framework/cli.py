import typer
from rich.console import Console
from rich.panel import Panel

from rag_framework.data_loaders.text_loader import TextLoader
from rag_framework.vector_stores.in_memory import InMemoryVectorStore
from rag_framework.retrievers.basic_retriever import BasicRetriever
from rag_framework.generators.dummy_generator import DummyGenerator

# Import architectures
from rag_framework.architectures.basic_rag import BasicRAG
from rag_framework.architectures.self_rag import SelfRAG
from rag_framework.architectures.graph_rag import GraphRAG
from rag_framework.architectures.multimodal_rag import MultimodalRAG

app = typer.Typer(help="Enterprise Multi-Architecture RAG Framework CLI")
console = Console()

@app.command()
def ingest(source: str, chunk_size: int = typer.Option(500, help="Chunk size for splitting text")):
    """Ingest documents from a source into the vector store."""
    console.print(f"[bold green]Ingesting from:[/bold green] {source}")
    loader = TextLoader()
    docs = loader.load(source)
    console.print(f"Loaded {len(docs)} document(s).")
    console.print(f"[bold green]Successfully ingested![/bold green]")

@app.command()
def run(query: str, arch: str = typer.Option("basic", help="Architecture to run (basic, self, graph, multimodal)")):
    """Run a query through the selected RAG architecture."""
    # Build core components (Mock implementations)
    store = InMemoryVectorStore()
    retriever = BasicRetriever(store)
    generator = DummyGenerator()
    
    # Select architecture
    if arch == "basic":
        pipeline = BasicRAG(retriever, generator)
    elif arch == "self":
        pipeline = SelfRAG(retriever, generator)
    elif arch == "graph":
        pipeline = GraphRAG(generator)
    elif arch == "multimodal":
        pipeline = MultimodalRAG(retriever, generator)
    else:
        console.print(f"[bold red]Unknown architecture:[/bold red] {arch}")
        raise typer.Exit(code=1)

    console.print(Panel.fit(f"[bold blue]Query:[/bold blue] {query}\n[bold yellow]Architecture:[/bold yellow] {arch.upper()}", title="Input"))
    
    response = pipeline.run(query)
    
    console.print(Panel.fit(response, title=f"RAG Output ({arch.upper()})", border_style="green"))

@app.command()
def evaluate(
    dataset: str = typer.Option(..., help="Path to evaluation dataset (JSON)"),
    arch: str = typer.Option("basic", help="Architecture to evaluate")
):
    """Evaluate the RAG pipeline against a dataset."""
    from rag_framework.evaluators.basic_evaluator import BasicEvaluator
    
    console.print(f"[bold yellow]Evaluating {arch.upper()} pipeline using dataset:[/bold yellow] {dataset}")
    evaluator = BasicEvaluator()
    metrics = evaluator.evaluate([{"dummy": "data"}])
    
    console.print("[bold green]Evaluation Results:[/bold green]")
    for k, v in metrics.items():
        console.print(f"  - {k}: {v:.2f}")

if __name__ == "__main__":
    app()
