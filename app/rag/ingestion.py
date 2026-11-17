
from pathlib import Path
from app.rag.vector_store import add_document

def load_documents():

    folders = {
        "trusted": Path(
            "app/data/knowledge_base/trusted"
        ),
        "untrusted": Path(
            "app/data/knowledge_base/untrusted"
        )
    }

    for trust_level, folder in folders.items():

        for file_path in folder.glob("*.txt"):

            text = file_path.read_text(
                encoding="utf-8"
            )

            doc_id = f"{trust_level}_{file_path.stem}"

            add_document(
                doc_id=doc_id,
                text=text,
                trust_level=trust_level
            )

            print("Loaded:", doc_id)

if __name__ == "__main__":
    load_documents()
