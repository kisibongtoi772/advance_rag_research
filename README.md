# Advance RAG Research Framework

## Abstract

The Advance RAG Research Framework is an enterprise-grade, modular architecture designed for the implementation, testing, and evaluation of advanced Retrieval-Augmented Generation (RAG) systems. The framework acts as a quantitative and qualitative testing ground to benchmark standard baseline RAG methodologies against highly optimized architectures, specifically Self-Reflective RAG (Self-RAG), Graph-based RAG (Graph-RAG), HyDE, and Self-Ask.

---

## 1. System Architecture

The codebase adheres strictly to Clean Architecture principles, employing the **Provider Factory** pattern to seamlessly hot-swap between major LLM vendors.

```text
advance_rag_research/
├── datasets/                 # Enterprise and Scientific benchmarking datasets
├── reports/                  # Evaluation metrics and architectural findings
├── src/
│   └── rag_framework/
│       ├── architectures/    # Core RAG Orchestration logic (Basic, Self, Graph, HyDE, Self-Ask)
│       ├── core/             # Pydantic domain models and Base Interfaces
│       ├── data_loaders/     # Data ingestion and preprocessing pipelines
│       ├── evaluators/       # Quantitative evaluation logic
│       ├── providers/        # LLM Provider Implementations (OpenAI, Anthropic, Google, Qwen, DeepSeek)
│       ├── retrievers/       # Information retrieval protocols
│       ├── vector_stores/    # Storage layers (e.g., ChromaDB, InMemory)
│       └── cli.py            # Command Line Interface application entry point
├── .agents/                  # Automated Agent Skills for auxiliary operations
└── pyproject.toml            # Python package configuration and dependencies
```

---

## 2. Prerequisites and Setup

The framework requires a standard Python environment and an active API key for the models you intend to test.

1. Ensure Python 3.10+ is installed on the host machine.
2. Export the required authentication keys based on your provider:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   export ANTHROPIC_API_KEY="your_api_key_here"
   export GEMINI_API_KEY="your_api_key_here"
   export DEEPSEEK_API_KEY="your_api_key_here"
   export DASHSCOPE_API_KEY="your_api_key_here" # For Qwen
   ```
3. Install the package dependencies in editable mode:
   ```bash
   pip install -e .
   ```

---

## 3. Execution Protocols (CLI)

The framework exposes a Typer-based CLI (`rag-framework`) for streamlined execution. It utilizes the `--arch` argument to select the RAG engine and `--provider` to select the LLM vendor.

### 3.1 Data Ingestion
Loads and indexes documents into the selected storage layer.
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py ingest datasets/corpus.json --chunk-size 500
```

### 3.2 Query Execution
Test specific queries against the designated RAG architectures across any provider.

**Standard Vector Search (Basic RAG)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "What is the QuantumX processor?" --arch basic --provider openai
```

**Anti-Hallucination Loop (Self-RAG)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "Who is the CEO of VisionAI?" --arch self --provider anthropic
```

**Multi-hop Entity Reasoning (Graph RAG)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "What product is made by the company acquired by NovaTech?" --arch graph --provider google
```

**Zero-Shot Query Expansion (HyDE RAG)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "How to optimize latent representations?" --arch hyde --provider deepseek
```

**Multi-hop Compositional Reasoning (Self-Ask RAG)**
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py run "Who was the president when the first moon landing happened?" --arch self_ask --provider qwen
```

### 3.3 Automated Evaluation
Executes the evaluator module to benchmark a specific architecture against a standardized JSON evaluation dataset.
```bash
PYTHONPATH=src python3 src/rag_framework/cli.py evaluate --dataset datasets/qa_eval.json --arch hyde --provider openai
```

---

## 4. Evaluation Methodology

The framework utilizes structured datasets to rigorously test hallucination resistance, factual accuracy, and context retrieval precision. Detailed findings and metrics are documented in the `reports/` directory.

- **reports/executive_summary.md**: High-level strategic architectural recommendations for production environments.
- **reports/detailed_metrics.md**: In-depth quantitative analysis of latency, token cost, and Ragas metrics.
- **reports/real_scientific_metrics.md**: Evaluation results specifically focusing on high-density academic and scientific text parsing.
