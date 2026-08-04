import os
import requests
from dotenv import load_dotenv

load_dotenv()


class EmbeddingModel:

    def __init__(self):
        self.api_key = os.getenv("JINA_API_KEY")

    def embed(self, text: str):

        response = requests.post(
            "https://api.jina.ai/v1/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "jina-embeddings-v3",
                "input": [text]
            },
            timeout=30
        )

        response.raise_for_status()

        return response.json()["data"][0]["embedding"]

    def embed_documents(self, documents: list[str]):

        response = requests.post(
            "https://api.jina.ai/v1/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "jina-embeddings-v3",
                "input": documents
            },
            timeout=60
        )

        response.raise_for_status()

        return [
            item["embedding"]
            for item in response.json()["data"]
        ]