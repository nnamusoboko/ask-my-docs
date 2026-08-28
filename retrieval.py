import logging
from typing import Callable
from rank_bm25 import BM25Okapi
from models import Chunk


logger = logging.getLogger(__name__)


class Retriever:

    @staticmethod
    def get_chunk_stats(chunk: str) -> dict[str, int | float | str]:
        """returns an index for chunk, score for the chunk, individual-stats for the words"""
        return {}

    @staticmethod
    def create_search_engine(
        chunks: list[Chunk],
        normalise_chunk_text: Callable[[list[Chunk]], list[Chunk]],
        tokenize_text: Callable[[str], list[str]],
    ) -> BM25Okapi:
        """BM25 mathematical index."""
        normalised_chunks = normalise_chunk_text(chunks)
        tokenized_chunks = [tokenize_text(chunk.content) for chunk in normalised_chunks]

        logger.info("Created search index with %d chunks", len(tokenized_chunks))

        return BM25Okapi(tokenized_chunks)


    @staticmethod
    def find_chunk(tokenized_user_query: list[str], chunks: list[Chunk], bm25: BM25Okapi) -> Chunk | None:
        if not chunks:
            raise ValueError("Cannot calculate stats because the chunks list is empty")

        question_word_tokens = tokenized_user_query
        scores = bm25.get_scores(question_word_tokens)
        best_score = int(scores.max())

        if best_score == 0:
            return None

        best_chunk_index = int(scores.argmax())

        logger.info("Query matched chunk #%d", best_chunk_index)

        return chunks[best_chunk_index]

    @staticmethod
    def calculate_word_scores(
        question: str,
        chunk_text: str,
        chunks: list[str],
        bm25: BM25Okapi,
        normalize_text: Callable[[str], str],
        tokenize_text: Callable[[str], list[str]],
    ) -> dict[str, float]:
        """ONLY calculate word scores using the engine."""
        matched_words: dict[str, float] = {}
        qtn_word_tokens = tokenize_text(normalize_text(question))
        winner_tokens = tokenize_text(normalize_text(chunk_text))

        # Find where the winner text lives in the original list to get its doc length
        chunk_index = chunks.index(chunk_text)

        for word in qtn_word_tokens:
            tf = winner_tokens.count(word)
            if tf == 0 or word not in bm25.idf:
                continue
            idf = bm25.idf[word]
            doc_len = bm25.doc_len[chunk_index]
            numerator = tf * (bm25.k1 + 1)
            denominator = tf + bm25.k1 * (1 - bm25.b + bm25.b * doc_len / bm25.avgdl)
            matched_words[word] = idf * numerator / denominator

        return matched_words
