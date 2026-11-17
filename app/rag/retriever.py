from app.rag.vector_store import search_document


def retrieve_knowledge(question):

    results = search_document(
        query=question,
        top_k=3
    )

    documents = results["documents"][0]
    metadata = results["metadatas"][0]
    ids = results["ids"][0]

    retrieved_data = []

    for doc_id, text, meta in zip(ids, documents, metadata):

        retrieved_data.append({
            "id": doc_id,
            "content": text,
            "trust_level": meta["trust_level"]
        })

    return retrieved_data


if __name__ == "__main__":

    question = "What is the company security policy?"

    results = retrieve_knowledge(question)

    for doc in results:
        print("\nDocument:", doc["id"])
        print("Trust:", doc["trust_level"])
        print("Content:", doc["content"])