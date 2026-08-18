def clean_words(text: str) -> list[str]:
    STOPWORDS = {"what", "is", "are", "of", "a", "an", "the"}
    stripped = [word.strip("?!.,;:()\"'") for word in text.lower().split()] 
    return [word for word in stripped if word not in STOPWORDS]


