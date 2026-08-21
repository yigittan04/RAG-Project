import pickle
import faiss
import numpy as np


class VectorStore:

    INDEX_PATH = "vector_store/faiss_index.bin"
    METADATA_PATH = "vector_store/metadata.pkl"

    def __init__(self):

        self.index = faiss.read_index(
            self.INDEX_PATH
        )

        with open(
            self.METADATA_PATH,
            "rb"
        ) as f:
            self.metadata = pickle.load(f)

    def add_chunks(
        self,
        embeddings,
        metadata
    ):

        embeddings = np.array(
            embeddings
        ).astype("float32")

        if len(embeddings) != len(metadata):
            raise ValueError(
                "Number of embeddings must match number of metadata records."
            )

        self.index.add(embeddings)

        self.metadata.extend(metadata)

    def save(self):

        faiss.write_index(
            self.index,
            self.INDEX_PATH
        )

        with open(
            self.METADATA_PATH,
            "wb"
        ) as f:
            pickle.dump(
                self.metadata,
                f
            )

    def search(
        self,
        embedding,
        top_k=3,
        document_id=None
    ):

        embedding = np.array(
            [embedding]
        ).astype("float32")

        search_k = self.index.ntotal

        if search_k == 0:
            return []

        scores, indices = self.index.search(
            embedding,
            search_k
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

            if document_id is not None:

                if metadata.get("document_id") != str(document_id):
                    continue

            results.append(
                {
                    "chunk_id": metadata["chunk_id"],
                    "document_id": metadata.get("document_id"),
                    "content": metadata["content"],
                    "similarity": float(score)
                }
            )

            if len(results) >= top_k:
                break

        return results