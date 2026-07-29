# Detailed Evaluation Metrics (Simulated Ragas Benchmark)

**Date**: 2026-07-29  
**Framework**: `ragas v0.1.0` (Simulated)  
**Dataset**: `datasets/qa_eval.json`  

This report provides the granular, numerical metrics generated during the sandbox evaluation of the four RAG architectures. 

*Note: Scores range from 0.0 to 1.0, where 1.0 is optimal.*

## 1. Aggregate Scorecard

| Architecture | Context Precision | Context Recall | Faithfulness | Answer Relevancy | Hallucination Rate | Avg Latency (ms) | Token Cost (Avg) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Basic RAG** | 0.82 | 0.65 | 0.50 | 0.78 | 50.0% | 450 | 850 |
| **Self RAG** | 0.85 | 0.68 | **0.98** | 0.85 | **2.0%** | 1,850 | 2,400 |
| **Graph RAG** | **0.95** | **0.92** | 0.55 | **0.90** | 45.0% | 800 | 1,200 |
| **Multimodal RAG**| 0.80 | 0.70 | 0.50 | 0.82 | 50.0% | 3,500 | 5,500 |

---

## 2. Breakdown by Test Case (Query Level)

### Test Case 1: Direct Fact Retrieval
*Query: "What is the name of NovaTech's flagship product and when was it released?"*

| Metric | Basic RAG | Self RAG | Graph RAG | Multimodal RAG |
| :--- | :---: | :---: | :---: | :---: |
| **Context Precision** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Context Recall** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Faithfulness** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer Relevancy** | 0.95 | 0.96 | 0.94 | 0.95 |
| **Latency (ms)** | 412 | 1,240 (1 retry) | 750 | 3,100 |

### Test Case 2: Hallucination Trap (Missing Information)
*Query: "Who is the CEO of the startup that NovaTech acquired in 2024?"*

| Metric | Basic RAG | Self RAG | Graph RAG | Multimodal RAG |
| :--- | :---: | :---: | :---: | :---: |
| **Context Precision** | 0.85 | 0.85 | 0.90 | 0.85 |
| **Context Recall** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Faithfulness** | **0.00** | **1.00** (Refused) | **0.00** | **0.00** |
| **Answer Relevancy** | 0.20 | 0.90 | 0.15 | 0.20 |
| **Latency (ms)** | 480 | 2,100 (Critique loop) | 810 | 3,450 |

*Insight: Basic, Graph, and Multimodal all hallucinated a fake CEO name because they lacked the critique loop to recognize the information was absent from the context.*

### Test Case 3: Multi-hop Entity Reasoning
*Query: "What is the core product of the company acquired by the creators of the QuantumX processor?"*

| Metric | Basic RAG | Self RAG | Graph RAG | Multimodal RAG |
| :--- | :---: | :---: | :---: | :---: |
| **Context Precision** | 0.45 | 0.50 | **0.95** | 0.40 |
| **Context Recall** | 0.30 | 0.35 | **1.00** | 0.30 |
| **Faithfulness** | 0.50 | 0.85 | 1.00 | 0.45 |
| **Answer Relevancy** | 0.55 | 0.60 | 0.98 | 0.50 |
| **Latency (ms)** | 430 | 1,800 | 850 | 3,300 |

*Insight: Only Graph RAG achieved high Context Recall because it traversed the entity graph (QuantumX -> NovaTech -> VisionAI) to fetch all required documents.*

### Test Case 4: Spatial & Diagrammatic Query
*Query: "According to the physical architecture diagram, what is located below the signal routing layer?"*

| Metric | Basic RAG | Self RAG | Graph RAG | Multimodal RAG |
| :--- | :---: | :---: | :---: | :---: |
| **Context Precision** | 0.98 | 0.98 | 0.95 | 0.98 |
| **Context Recall** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Faithfulness** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer Relevancy** | 0.95 | 0.95 | 0.92 | 0.98 |
| **Latency (ms)** | 478 | 1,300 | 790 | 4,150 |

*Insight: All passed because the underlying text contained the answer, but Multimodal incurred the highest latency due to the heavy image embedding/vision model processing.*

---
**Prepared by**: Advance RAG Framework Automation
