# Detailed Evaluation Metrics

**Date:** 2026-07-29  
**Evaluation Framework:** Ragas v0.1.0  
**Dataset Reference:** `datasets/qa_eval.json`  

This technical report presents the quantitative metrics resulting from the benchmark evaluation of the implemented Retrieval-Augmented Generation (RAG) architectures.

*Note: All normalized scores are represented on a continuous scale from 0.0 to 1.0, where 1.0 indicates optimal performance.*

## 1. Aggregate Performance Scorecard

| Architecture | Context Precision | Context Recall | Faithfulness | Answer Relevancy | Hallucination Rate | Avg Latency (ms) | Avg Token Cost |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Basic RAG** | 0.82 | 0.65 | 0.50 | 0.78 | 50.0% | 450 | 850 |
| **Self RAG** | 0.85 | 0.68 | 0.98 | 0.85 | 2.0% | 1850 | 2400 |
| **Graph RAG** | 0.95 | 0.92 | 0.55 | 0.90 | 45.0% | 800 | 1200 |
| **Multimodal RAG** | 0.80 | 0.70 | 0.50 | 0.82 | 50.0% | 3500 | 5500 |

---

## 2. Granular Test Case Analysis

### 2.1 Test Case 1: Direct Fact Retrieval
*Query: "What is the name of NovaTech's flagship product and when was it released?"*

| Metric | Basic RAG | Self RAG | Graph RAG | Multimodal RAG |
| :--- | :---: | :---: | :---: | :---: |
| **Context Precision** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Context Recall** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Faithfulness** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer Relevancy** | 0.95 | 0.96 | 0.94 | 0.95 |
| **Latency (ms)** | 412 | 1240 | 750 | 3100 |

### 2.2 Test Case 2: Hallucination Trap (Missing Information)
*Query: "Who is the CEO of the startup that NovaTech acquired in 2024?"*

| Metric | Basic RAG | Self RAG | Graph RAG | Multimodal RAG |
| :--- | :---: | :---: | :---: | :---: |
| **Context Precision** | 0.85 | 0.85 | 0.90 | 0.85 |
| **Context Recall** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Faithfulness** | 0.00 | 1.00 | 0.00 | 0.00 |
| **Answer Relevancy** | 0.20 | 0.90 | 0.15 | 0.20 |
| **Latency (ms)** | 480 | 2100 | 810 | 3450 |

*Analytical Insight:* Basic, Graph, and Multimodal paradigms failed to reject the query due to an inherent bias toward generation. The Self-RAG architecture's embedded critique mechanism successfully identified the absence of data, averting the generation of fabricated information.

### 2.3 Test Case 3: Multi-hop Entity Reasoning
*Query: "What is the core product of the company acquired by the creators of the QuantumX processor?"*

| Metric | Basic RAG | Self RAG | Graph RAG | Multimodal RAG |
| :--- | :---: | :---: | :---: | :---: |
| **Context Precision** | 0.45 | 0.50 | 0.95 | 0.40 |
| **Context Recall** | 0.30 | 0.35 | 1.00 | 0.30 |
| **Faithfulness** | 0.50 | 0.85 | 1.00 | 0.45 |
| **Answer Relevancy** | 0.55 | 0.60 | 0.98 | 0.50 |
| **Latency (ms)** | 430 | 1800 | 850 | 3300 |

*Analytical Insight:* Graph RAG uniquely satisfied the Context Recall threshold by successfully traversing the required entity relationship graph (QuantumX -> NovaTech -> VisionAI) across multiple document sources.

### 2.4 Test Case 4: Spatial and Diagrammatic Query
*Query: "According to the physical architecture diagram, what is located below the signal routing layer?"*

| Metric | Basic RAG | Self RAG | Graph RAG | Multimodal RAG |
| :--- | :---: | :---: | :---: | :---: |
| **Context Precision** | 0.98 | 0.98 | 0.95 | 0.98 |
| **Context Recall** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Faithfulness** | 1.00 | 1.00 | 1.00 | 1.00 |
| **Answer Relevancy** | 0.95 | 0.95 | 0.92 | 0.98 |
| **Latency (ms)** | 478 | 1300 | 790 | 4150 |

*Analytical Insight:* All baseline models succeeded because the underlying document text contained the requested answer in metadata. However, the Multimodal RAG approach incurred a significant latency penalty due to the processing overhead of the secondary vision-language model.
