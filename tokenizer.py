def tokenize_normalised_text(normalized_text: str) -> list[str]:
    """Transforms a pre-normalized text string into clean keyword tokens."""
    if not normalized_text:
        return []

    raw_words = normalized_text.split()

    return raw_words
