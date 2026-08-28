import logging
import re
import string
from models import Chunk


logger = logging.getLogger(__name__)

PUNCT_TABLE = str.maketrans("", "", string.punctuation)


class TextCleaner:

    @staticmethod
    def clean_document_text(text: str) -> str:
        if not text:
            raise ValueError("Document has no content")

        text = text.replace("\ufeff", "")
        text = "".join(ch for ch in text if ch == "\n" or ord(ch) >= 32)
        text = re.sub(r"(?<=\S) {2,}(?=\S)", " ", text)

        logger.info("Cleaned document (len: %d)", len(text))

        return text


    @staticmethod
    def normalise_text(text: str) -> str:
        """Lowercases text and strips all punctuation symbols"""
        if not text:
            return ""

        return text.lower().translate(PUNCT_TABLE)

    @staticmethod
    def normalise_chunk_text(chunks: list[Chunk]) -> list[Chunk]:
        if not chunks:
            return []

        return [
            Chunk(
                content=TextCleaner.normalise_text(chunk.content),
                metadata=chunk.metadata
            )
            for chunk in chunks
        ]
