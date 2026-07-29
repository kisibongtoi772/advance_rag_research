# Advance RAG Research Framework

An Enterprise-grade, modular, and clean-architecture framework designed to build, test, and evaluate advanced Retrieval-Augmented Generation (RAG) systems. This project serves as a testing ground to benchmark standard RAG against highly optimized agentic architectures like Self-RAG and Graph-RAG.

---

## 🏗️ Project Structure

The codebase strictly adheres to Clean Architecture, segregating interfaces, core logic, and specific architectural implementations.

```text
advance_rag_research/
├── datasets/                 # Synthetic datasets (Corpus & QA Evaluation pairs)
├── reports/                  # Benchmark and architectural evaluation reports
│   ├── detailed_metrics.md
│   └── executive_summary.md
├── src/
│   └── rag_framework/
│       ├── architectures/    # Core RAG Orchestrations
│       │   ├── base.py
│       │   ├── basic_rag.py  # Standard Vector Search
│       │   ├── graph_rag.py  # Knowledge Graph Traversal
│       │   ├── multimodal_rag.py # Vision/Image processing
│       │   └── self_rag.py   # Critique & Retry Loop
│       ├── core/             # Pydantic domain models & Base Interfaces
│       ├── data_loaders/     # Ingestion pipelines
│       ├── embeddings/       # Embedding models (e.g., OpenAI, HuggingFace)
│       ├── evaluators/       # Ragas-based evaluation logic
│       ├── generators/       # LLM generation wrappers
│       ├── retrievers/       # Retrieval logic
│       ├── vector_stores/    # ChromaDB, InMemory, Pinecone, etc.
│       └── cli.py            # Typer CLI application entry point
├── .agents/skills/           # Automated Agent Skills (Git, Literature Search, etc.)
└── pyproject.toml            # Python package configuration
```

---

## 🚀 Installation & Setup

1. **Ensure Python 3.10+ is installed.**
2. **Install the package in editable mode:**
   ```bash
   pip install -e .
   ```
   *(Alternatively, if dependencies expand, use `pip install -r requirements.txt` or `poetry install`)*

---

## 💻 Usage (CLI Operations)

The framework exposes a smart Typer CLI `rag-framework` (or you can run `cli.py` directly). It uses the `--arch` flag to seamlessly switch between the underlying RAG engines.

### 1. Ingesting Data
Load and index documents into the Vector/Graph Store.
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py ingest datasets/corpus.json --chunk-size 500
```

### 2. Running Queries
Test how different architectures handle specific questions.

**Test Basic RAG (Vector Search)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "What is the QuantumX processor?" --arch basic
```

**Test Self-RAG (Anti-Hallucination)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "Who is the CEO of VisionAI?" --arch self
```
*(Watch the console log as it critiques itself and refuses to hallucinate an answer).*

**Test Graph RAG (Multi-hop Entity Reasoning)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "What product is made by the company acquired by NovaTech?" --arch graph
```

**Test Multimodal RAG (Diagram Analysis)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "What layer is at the bottom of Fig-A?" --arch multimodal
```

### 3. Running Automated Evaluation
Run the evaluator module to benchmark a specific architecture against a JSON evaluation dataset.
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py evaluate --dataset datasets/qa_eval.json --arch self
```

---

## 📊 Evaluation Reports

We have conducted a thorough synthetic benchmark utilizing the `datasets/qa_eval.json` to measure *Context Precision*, *Context Recall*, *Faithfulness*, and *Hallucination Rates*.

- **[Executive Summary](reports/executive_summary.md)**: High-level overview and strategic recommendations for Enterprise deployment (Recommends a hybrid `Graph-Self-RAG` approach).
- **[Detailed Metrics](reports/detailed_metrics.md)**: In-depth numerical breakdown of latency, token cost, and Ragas metrics for each test case.
