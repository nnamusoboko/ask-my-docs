from rank_bm25 import BM25Okapi
from cleaning import clean_words, best_chunk_stats

def find_relevant_chunk(question: str, chunks: list[str]) -> tuple[float, str, dict[str, float]]:
    if not chunks:
        return 0, "", {}

    question_word_tokens = clean_words(question)

    best_chunk = ""
    best_score = 0
    matched_words = {}

    tokenized_chunks = [clean_words(chunk) for chunk in chunks]

    bm25 = BM25Okapi(tokenized_chunks)
    scores = bm25.get_scores(question_word_tokens)

    best_score = scores.max()

    if best_score == 0:
        return 0, "", {}

    best_chunk_index = scores.argmax()
    best_chunk = chunks[best_chunk_index]

    winner_tokens = tokenized_chunks[best_chunk_index]
    matched_words = best_chunk_stats(bm25, winner_tokens, question_word_tokens, int(best_chunk_index))

    return best_score, best_chunk, matched_words
