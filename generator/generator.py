from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class Generator:

    @staticmethod
    def answer(question: str, context: str):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content":
                    (
                        "You are a Retrieval-Augmented Generation assistant. "
                        "Answer ONLY using the provided context. "
                        "If the answer is not contained in the context, say you do not know."
                    )
                },
                {
                    "role": "user",
                    "content":
                    f"Context:\n{context}\n\nQuestion:\n{question}"
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content