import logging

from numpy import index_exp
import constants
from models import Chunk


logger = logging.getLogger(__name__)

class Chunker:

    @staticmethod
    def fixed_size_chunking(
        text: str, chunk_size: int = constants.CHUNK_SIZE,
        overlap: int = constants.CHUNK_OVERLAP
    ) -> list[Chunk]:

        if overlap >= chunk_size:
            raise ValueError(f"Overlap {overlap} cant be greater or equal to {chunk_size}")
        text_len = len(text)
        chunks: list[Chunk] = []
        start = 0
        chunk_index = 0
        while start < text_len:
            end = min(start + chunk_size, text_len)
            chunk = text[start:end]
            chunks.append(Chunk(content=chunk, metadata={"index": chunk_index}))
            start += chunk_size - overlap
            chunk_index += 1

        logger.info("Chunking by fixed size: %d chunks", len(chunks))

        return chunks

    @staticmethod
    def chunk_by_structure(text: str, max_size: int = constants.MAX_SUB_SPLIT_SIZE) -> list[Chunk]:
        lines = text.splitlines()
        sections: list[str] = []
        current: list[str] = []

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

        glued_chunks = Chunker._glue_short_chunks(sections)
        final_chunks = Chunker._sub_split_chunks(glued_chunks, max_size)

        chunks = [
            Chunk(content=chunk, metadata={"index": index})
            for index, chunk in enumerate(final_chunks)
        ]

        logger.info("Chunking by structure: (%d chunks) (%d sections)", len(chunks), len(sections))

        return chunks

    @staticmethod
    def _glue_short_chunks(sections: list[str], threshold: int = constants.THRESHOLD) -> list[str]:
        """Combine section titles to content"""
        glued: list[str] = []

        for section in sections:
            if glued and len(glued[-1]) <= threshold:
                glued[-1] += "\n" + section
            else:
                glued.append(section)

        return glued

    @staticmethod
    def _sub_split_chunks(chunks: list[str], max_size: int) -> list[str]:
        """Split sections that are too large to balance chunks"""
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
