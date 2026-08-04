from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-MiniLM-L3-v2"
        )

    def embed(self, text: str):
        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def embed_documents(self, documents):
        return self.model.encode(
            documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
            batch_size=16
        )