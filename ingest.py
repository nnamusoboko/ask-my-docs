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

    
def chunk_by_structure(text: str) -> list[str]:
    # STEP 1: split into lines, find separator lines (=====)
    # STEP 2: group lines into blocks
    # STEP 3: drop separators, pair header block with its content
    
    lines = text.splitlines()
    sections = []
    current = []

    for line in lines:
        if line.strip() == "=====":
            if current:
                sections.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    return sections


def main():
    text = load_text("data/sample.txt")
    chunks = chunk_text(text, chunk_size=4, overlap=2)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {len(chunk)} chars -> {chunk}")

if __name__ == "__main__":
    main()
