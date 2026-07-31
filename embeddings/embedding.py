from sentence_transformers import SentenceTransformer

class EmbeddingModel:

    def __init__(self):

        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-MiniLM-L3-v2"
        )
    
    def embed(self, text: str):

        embedding = self.model.encode(text)

        return embedding

    def embed_documents(self, documents: list[str]):

        embeddings = self.model.encode(documents)

        return embeddings