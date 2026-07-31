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

faiss.normalize_L2(embeddings)

index.add(embeddings)

os.makedirs("database", exist_ok=True)

faiss.write_index(index, "database/faiss_index.bin")

with open("database/metadata.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Index saved.")