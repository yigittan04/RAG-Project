class PromptBuilder:

    @staticmethod
    def build(context_chunks, question, conversation_history=None):

        context = "\n\n".join(context_chunks)

        history = ""

        if conversation_history:
            history_lines = []

            for message in conversation_history:
                history_lines.append(
                    f"{message.role.capitalize()}: {message.content}"
                )

            history = "\n".join(history_lines)

        prompt = f"""Conversation history:
{history}

Retrieved context:
{context}

Current question:
{question}
"""

        return prompt