import pickle
import faiss
import numpy as np
import os


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

        for i, vector in enumerate(embeddings):
            metadata[i]["embedding"] = vector.tolist()

        self.index.add(
            embeddings
        )

        self.metadata.extend(
            metadata
        )

    def save(self):

        index_temp_path = (
            self.INDEX_PATH + ".tmp"
        )

        metadata_temp_path = (
            self.METADATA_PATH + ".tmp"
        )

        try:

            faiss.write_index(
                self.index,
                index_temp_path
            )

            with open(
                metadata_temp_path,
                "wb"
            ) as f:
                pickle.dump(
                    self.metadata,
                    f
                )

            os.replace(
                index_temp_path,
                self.INDEX_PATH
            )

            os.replace(
                metadata_temp_path,
                self.METADATA_PATH
            )

        except Exception:

            if os.path.exists(index_temp_path):
                os.remove(index_temp_path)

            if os.path.exists(metadata_temp_path):
                os.remove(metadata_temp_path)

            raise

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

    def delete_document(
        self,
        document_id
    ):

        document_id = str(document_id)

        remaining_metadata = [
            metadata
            for metadata in self.metadata
            if metadata.get("document_id") != document_id
        ]

        if len(remaining_metadata) == len(self.metadata):
            return False

        if remaining_metadata:

            embeddings = np.array(
                [
                    metadata["embedding"]
                    for metadata in remaining_metadata
                ],
                dtype="float32"
            )

            dimension = embeddings.shape[1]

            self.index = faiss.IndexFlatIP(
                dimension
            )

            self.index.add(
                embeddings
            )

        else:

            dimension = self.index.d

            self.index = faiss.IndexFlatIP(
                dimension
            )

        self.metadata = remaining_metadata

        return True