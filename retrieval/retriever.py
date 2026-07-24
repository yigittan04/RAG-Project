import numpy as np

class Retriever:

    @staticmethod
    def cosine_similarity(vector_a, vector_b):

        dot_product = np.dot(vector_a, vector_b)
        
        norm_a = np.linalg.norm(vector_a)
        
        norm_b = np.linalg.norm(vector_b)

        similarity = dot_product / (norm_a * norm_b)

        return similarity
    
    @staticmethod
    def retrieve(
        question_embedding,
        chunk_embeddings,
        chunks,
        top_k=3
    ):
        results = []
        for chunk, embedding in zip(chunks, chunk_embeddings):
            similarity = Retriever.cosine_similarity(
            question_embedding,
            embedding
            )
            if similarity >= 0.7:
                results.append((similarity, chunk))
        results.sort(key=lambda x: x[0], reverse=True)
        top_results = results[:top_k]
        return top_results