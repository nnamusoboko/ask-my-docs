import logging

logger = logging.getLogger(__name__)

MAX_SUB_SPLIT_SIZE = 500
CHUNK_OVERLAP = 100
CHUNK_SIZE = 500
THRESHOLD = 100
STOP_WORDS = {
    "what", "is", "are", "of", "a", "an", "the",

    "about", "above", "after", "again", "all", "am", "any", "at",
    "be", "because", "been", "before", "by", "for", "from",

    "how", "i", "my", "me", "we", "our", "you", "your", "this", "that",
    "which", "who", "whom", "with", "whats"
}

if not STOP_WORDS:
    raise ValueError("STOP_WORDS is empty")

if CHUNK_OVERLAP >= CHUNK_SIZE:
    raise ValueError("CHUNK_SIZE must be greater than CHUNK_OVERLAP")

if THRESHOLD < 0:
    raise ValueError("THRESHOLD is less than 0")

if MAX_SUB_SPLIT_SIZE < 0:
    raise ValueError("MAX_SUB_SPLIT_SIZE is less than 0")
