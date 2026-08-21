class TextChunker:

    @staticmethod
    def chunk_by_paragraph(text: str) -> list[str]:

        chunks = []

        paragraphs = text.split("\n\n")

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if paragraph:
                chunks.append(paragraph)
        
        return chunks

    @staticmethod
    def chunk_by_words(
        text: str,
        chunk_size: int = 200,
        overlap: int = 40
    ) -> list[str]:

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size.")

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):

            current_chunk = words[start:start + chunk_size]

            chunks.append(" ".join(current_chunk))

            start += chunk_size - overlap

        return chunks
