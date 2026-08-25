import logging

import constants

logger = logging.getLogger(__name__)


_STOPWORDS = {word.lower() for word in constants.STOP_WORDS}

def tokenize_normalised_text(normalized_text: str) -> list[str]:
    """Transforms a pre-normalized text string into clean keyword tokens."""
    if not normalized_text:
        logger.warning("normalized_text is empty")
        return []

    # tokenize and remove stopwords
    tokenized_string = [word for word in normalized_text.split() if word not in _STOPWORDS]

    return tokenized_string
