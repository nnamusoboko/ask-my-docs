import re
import string

import constants

PUNCT_TABLE = str.maketrans("", "", string.punctuation)
STOP_WORDS = constants.STOP_WORDS


class TextCleaner:

    @staticmethod
    def clean_document_text(text: str) -> str:
        if not text:
            raise ValueError("Document has no content")

        text = text.replace("\ufeff", "")
        text = "".join(ch for ch in text if ch == "\n" or ord(ch) >= 32)
        text = re.sub(r"(?<=\S) {2,}(?=\S)", " ", text)

        return text


    @staticmethod
    def normalise_text(text: str) -> str:
        """Lowercases text, removes stop words and strips all punctuation symbols"""
        if not text:
            return ""

        none_stopwords = [word for word in text.split() if word not in STOP_WORDS]
        text = " ".join(none_stopwords)

        return text.lower().translate(PUNCT_TABLE)

    @staticmethod
    def normalise_chunk_text(chunks: list[str]) -> list[str]:
        if not chunks:
            return []

        return [TextCleaner.normalise_text(chunk) for chunk in chunks]
