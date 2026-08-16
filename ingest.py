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


def chunk_by_structure(text: str, max_size: int = 500) -> list[str]:
    lines = text.splitlines()
    sections = []
    current = []

    for line in lines:
        doc_line = line.strip()
        if doc_line and set(doc_line) == {"="}:
            if current:
                sections.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    glued_chunks = glue_short_chunks(sections)
    final_chunks = sub_split_chunks(glued_chunks, max_size)

    return final_chunks

def glue_short_chunks(chunks: list[str], threshold: int = 100) -> list[str]:
    glued: list[str] = []

    for chunk in chunks:
        if glued and len(glued[-1]) <= threshold:
            glued[-1] += "\n" + chunk
        else:
            glued.append(chunk)

    return glued


def sub_split_chunks(chunks: list[str], max_size: int) -> list[str]:
    pieces: list[str] = []

    for chunk in chunks:
        chunk_len = len(chunk)
        if chunk_len <= max_size:
            pieces.append(chunk)
        else:
            start = 0
            while start < chunk_len:
                end = min(start + max_size, chunk_len)
                sub_chunk = chunk[start:end]
                pieces.append(sub_chunk)
                start += max_size

    return pieces


def main():
    text = load_text("data/sample.txt")
    chunks = chunk_text(text, chunk_size=4, overlap=2)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {len(chunk)} chars -> {chunk}")

if __name__ == "__main__":
    main()
