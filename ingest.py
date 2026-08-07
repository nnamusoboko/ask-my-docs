def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError(f"Overlap {overlap} cant be greater or equal to {chunk_size}")
    text_len = len(text);
    chunks = []
    start = 0
    while start < text_len: 
        end = min(start + chunk_size, text_len)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap 
    return chunks

def main():
    text = load_text("data/sample.txt")
    chunks = chunk_text(text, chunk_size=4, overlap=2)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {len(chunk)} chars -> {chunk}")

if __name__ == "__main__":
    main()
