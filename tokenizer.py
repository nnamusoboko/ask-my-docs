import constants

def tokenize_normalised_text(normalized_text: str) -> list[str]:
    """Transforms a pre-normalized text string into clean keyword tokens."""
    if not normalized_text:
        return []

    stopwords = {word.lower() for word in constants.STOP_WORDS}
    # tokenize and remove stopwords
    tokenized_string = [word for word in normalized_text.split() if word not in stopwords]

    return tokenized_string
