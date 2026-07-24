import numpy as np
from preprocessing.loader import DocumentLoader
from preprocessing.cleaner import TextCleaner
from preprocessing.chunker import TextChunker
from embeddings.embedding import EmbeddingModel
from retrieval.retriever import Retriever


text = DocumentLoader.load("data/test.txt")

clean_text = TextCleaner.clean(text)

chunks = TextChunker.chunk_by_paragraph(clean_text)

model = EmbeddingModel()

embeddings = model.embed_documents(chunks)

question = "What is Python?"

question_embedding = model.embed(question)

retrieved_chunks = Retriever.retrieve(
    question_embedding,
    embeddings,
    chunks,
    top_k=3
)

print("Question:", question)
print()

for score, chunk in retrieved_chunks:
    print(f"{score:.4f}")
    print(chunk)
    print("-" * 40)