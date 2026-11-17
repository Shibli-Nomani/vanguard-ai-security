# Vanguard AI Security

## Linux Command
- Acitvate WSL from terminal
```sh
wsl -l -v
wsl -d Ubuntu-20.04 

```
```sh
touch readme.md
nano readme.md
<ctrl+o ENTER ctrl+x>
/vanguard-ai-security/$ mkdir app chroma_db reports tests 
$ cd app
/vanguard-ai-security/app$ mkdir core targets engines rag agents data api

$ nano app/data/attack_scenarios.json

$ touch app/__init__.py
$ touch app/data/__init__.py
$ touch app/engines/__init__.py
$ touch app/core/__init__.py
$ touch app/targets/__init__.py
$ app/api/__init__.py

```

## Virtual Environment and Python 
- windows cmd
```sh
python -m venv env
env\Scripts\activate
pyenv local 3.10.8

```
```sh
pip install -r requirements.txt
```
# Stage - 1: Core Engine + ChromaDB foundation

## Step-01 : Create synthetic documents (RAG implementation)
The security problem is not simply that ChromaDB retrieved a document. The problem occurs if the application treats retrieved instructions as trusted instructions.

- create app/data/knowledge_base/trusted/company_policy.txt
  - Company Security Policy (AI agents must follow tool permission policies.)
- create app/data/knowledge_base/untrusted/unknown_document.txt:
  - This document contains an untrusted instruction. 

## Step-02 : Create the ChromaDB vector store

**File: app/rag/vector_store.py**

- SentenceTransformerEmbeddingFunction
- "all-MiniLM-L6-v2"
- search docs top_k=3

## Step-03: Build document ingestion

**File: app/rag/ingestion.py**

```sh
python -m app.rag.retriever
```

Synthetic Documents
        |
        v
    ingestion.py
        |
        v
    add_document()
        |
        v
      ChromaDB
        |
        v
  search_document()
        |
        v
    retriever.py
        |
        v
 Retrieved Documents
 (ID + Content + Trust)

 **Note: Prepared only retriever.py ingestion.py vector_store.py** 
```sh
python -m app.rag.ingestion
python -m app.rag.retriever
```
 ![alt text](image.png)

![alt text](image-1.png)
# Stage 2 — Block 1: Connect Groq LLM

## Step-1: Real LLM + RAG Security


