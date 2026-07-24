import re

class TextCleaner:

    @staticmethod
    def clean(text:str) -> str:

        lines = [line.strip() for line in text.splitlines()]

        text = "\n".join(lines)

        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()