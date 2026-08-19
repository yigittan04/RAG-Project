import pickle
import faiss
import numpy as np


class VectorStore:

    def __init__(self):

        self.index = faiss.read_index(
            "vector_store/faiss_index.bin"
        )

        with open(
            "vector_store/metadata.pkl",
            "rb"
        ) as f:
            self.metadata = pickle.load(f)


    def search(
        self,
        embedding,
        top_k=3
    ):

        embedding = np.array(
            [embedding]
        ).astype("float32")
        
        top_k = min(top_k, self.index.ntotal)

        scores, indices = self.index.search(
            embedding,
            top_k
        )

        results = []

        SIMILARITY_THRESHOLD = 0.70

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            if score < SIMILARITY_THRESHOLD:
                continue

            metadata = self.metadata[idx]

            results.append(
                {
                    "chunk_id": metadata["chunk_id"],
                    "content": metadata["content"],
                    "similarity": float(score)
                }
            )

        return results