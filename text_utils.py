from rank_bm25 import BM25Okapi

def clean_words(text: str) -> list[str]:
    return [word.strip("?!.,;:()\"'") for word in text.lower().split()]

def best_chunk_stats(bm25: BM25Okapi, winner_tokens: list[str], qtn_word_tokens: list[str], best_chunk_index: int) -> dict[str, float]:
    matched_words = {}
    for word in qtn_word_tokens:
        tf = winner_tokens.count(word)
        if tf == 0 or word not in bm25.idf:
            continue
        idf = bm25.idf[word]
        doc_len = bm25.doc_len[best_chunk_index]
        numerator = tf * (bm25.k1 + 1)
        denominator = tf + bm25.k1 * (1 - bm25.b + bm25.b * doc_len / bm25.avgdl)
        matched_words[word] = idf * numerator /denominator

    return matched_words


