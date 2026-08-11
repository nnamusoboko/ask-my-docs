def clean_words(text: str) -> list[str]:
    return [word.strip("?!.,;:()\"'") for word in text.lower().split()]
