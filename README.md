# Fashion Semantic Search Project

## 🧵 Introduction

This project explores **building a semantic search and retrieval-augmented QA system** on a collection of fashion-related PDF documents using Databricks.  
The goal: **quickly find the most relevant passages and answer complex questions from diverse documents, even if wording or format varies.**

### **Why?**
- Traditional keyword search often fails when users don’t know exact phrases or when answers are scattered across large/unstructured documents.
- Semantic (vector-based) search leverages machine learning to find *meaning*, not just matching words—unlocking new workflows for research, discovery, and automation.

---

## 🚦 Project Plan & Workflow

1. **Read & Ingest**  
   Load PDF documents (fashion industry, sustainability, transparency, etc.) into Spark DataFrames.

2. **Chunking**  
   Split long texts into smaller, overlapping chunks for better semantic granularity and recall.

3. **Embedding**  
   Use a transformer-based model (e.g., `all-MiniLM-L6-v2`) to convert each chunk into a high-dimensional embedding vector.

4. **(Optional: OpenAI Attempt)**  
   Attempted to use OpenAI embeddings (documented in case of future troubleshooting).

5. **Vector Indexing**  
   Create a vector index (using Databricks Vector Search) on the embeddings, enabling fast semantic similarity search.

6. **Semantic Search**  
   Query the index with user questions, returning the top relevant text chunks from the corpus.

7. **QA (Question Answering)**  
   Optionally, pass top results to an LLM for natural language answers grounded in the source material.

---

## 📁 Folder Overview

- `0_read`  
  PDF ingestion and parsing scripts/notebooks.

- `1_chunk`  
  Chunking logic and code.

- `2_embed`  
  Embedding generation using Sentence Transformers (and variants).

- `2_Failed_OpenAiEmbed`  
  Documentation and code for the OpenAI embedding attempt.

- `3_vector`  
  Vector index creation and semantic search queries.

- `4_QA`  
  Retrieval-augmented QA workflows.

- `README.md`  
  (This file) — motivation, workflow, and usage.

---

## 📝 Notes

- **Platform:** Databricks with Unity Catalog and Vector Search enabled.
- **Flexibility:** All steps are modular—swap chunking or embedding models, adapt for new document types, etc.
- **Lessons Learned:** OpenAI embedding workflow was documented but not used due to API quota/plan limits.

---

## 🔧 Requirements

- Databricks workspace (Vector Search enabled)
- Python 3.10+
- Access to HuggingFace or compatible embedding models
- (Optional) API keys for remote embedding (OpenAI/HuggingFace)

---

## 💡 Author & License

Project by Zahra Roozbehi, 2025  

---
