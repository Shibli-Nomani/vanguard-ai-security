
import chromadb

from chromadb.utils import embedding_functions


# Persistent ChromaDB database
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Embedding model
embedding_function = (
    embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
)

# Collection
collection = client.get_or_create_collection(
    name="sentinel_knowledge",
    embedding_function=embedding_function
)


def add_document(doc_id, text, trust_level):

    collection.upsert(
        ids=[doc_id],
        documents=[text],
        metadatas=[{
            "trust_level": trust_level
        }]
    )


def search_document(query, top_k=3):

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    return results

