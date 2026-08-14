from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


class Generator:

    @staticmethod
    def answer(prompt: str):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content":
                    (
                        "You are a Retrieval-Augmented Generation assistant. "
                        "Answer ONLY using the provided retrieved context. "
                        "Use the conversation history only to understand references and follow-up questions. "
                        "Do not use the conversation history as a source of factual information. "
                        "If the answer is not contained in the retrieved context, say you do not know."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content