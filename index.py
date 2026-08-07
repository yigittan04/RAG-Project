import os
import pickle
import faiss
import numpy as np

from preprocessing.loader import DocumentLoader
from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker
from embeddings.embedding import EmbeddingModel

print("Loading documents...")

text = DocumentLoader.load("data/test.txt")

clean_text = TextCleaner.clean(text)

chunks = TextChunker.chunk_by_paragraph(clean_text)

print(f"Created {len(chunks)} chunks.")

model = EmbeddingModel()

embeddings = model.embed_documents(chunks)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

os.makedirs("vector_store", exist_ok=True)

faiss.write_index(index, "vector_store/faiss_index.bin")

with open("vector_store/metadata.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Index saved.")