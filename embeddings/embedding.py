from sentence_transformers import SentenceTransformer

class EmbeddingModel:

    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
    
    def embed(self, text: str):

        embedding = self.model.encode(text)

        return embedding

    def embed_documents(self, documents: list[str]):

        embeddings = self.model.encode(documents)

        return embeddings