import os
import pickle
import hashlib
import faiss
import numpy as np
from preprocessing.loader import DocumentLoader
from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker
from embeddings.embedding import EmbeddingModel
from database.database import SessionLocal
from database.models import Document, Chunk


DOCUMENT_PATH = "data/test.txt"


print("Loading documents...")

text = DocumentLoader.load(DOCUMENT_PATH)

clean_text = TextCleaner.clean(text)

chunks = TextChunker.chunk_by_paragraph(clean_text)

print(f"Created {len(chunks)} chunks.")

model = EmbeddingModel()

embeddings = model.embed_documents(chunks)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

uploaded_by="f8c06c99-31b7-498f-9260-69fbff3b2e75"

db = SessionLocal()

try:
    with open(DOCUMENT_PATH, "rb") as f:
        file_data = f.read()

    file_hash = hashlib.sha256(file_data).hexdigest()

    document = Document(
        filename=os.path.basename(DOCUMENT_PATH),
        uploaded_by=uploaded_by,
        total_chunks=len(chunks),
        file_size=os.path.getsize(DOCUMENT_PATH),
        mime_type="text/plain",
        storage_path=DOCUMENT_PATH,
        file_hash=file_hash,
        status="processed"
    )

    db.add(document)
    db.flush()

    chunk_records = []

    for i, chunk_text in enumerate(chunks):

        chunk = Chunk(
            document_id=document.id,
            chunk_index=i,
            page_number=None,
            content=chunk_text
        )

        db.add(chunk)
        chunk_records.append(chunk)

    db.commit()

    print(f"Created document: {document.id}")
    print(f"Created {len(chunk_records)} database chunks.")


    metadata = [
        {
            "chunk_id": str(chunk.id),
            "content": chunk.content
        }
        for chunk in chunk_records
    ]

    os.makedirs("vector_store", exist_ok=True)

    faiss.write_index(
        index,
        "vector_store/faiss_index.bin"
    )

    with open(
        "vector_store/metadata.pkl",
        "wb"
    ) as f:
        pickle.dump(metadata, f)

    print("Index saved.")


except Exception:
    db.rollback()
    raise

finally:
    db.close()