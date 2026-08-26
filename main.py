from logger_config import setup_logging
from loader import load_text
from cleaning import TextCleaner
from chunking import Chunker
from tokenizer import tokenize_normalised_text
from retrieval import Retriever
from generation import ask_model
from cli import get_cli_args
from config import Config

setup_logging()

def main() -> None:
    args = get_cli_args()

    file = args["file"]
    overlap = args["overlap"]
    max_tokens = args["max_tokens"]
    chunker = args["chunker"]
    chunk_size = args["chunk_size"]
    user_questions = args["questions"]

    text = load_text(file)
    clean_doc_text = TextCleaner.clean_document_text(text)
    chunks: list[str] = []

    if chunker == "structured":
        chunks = Chunker.chunk_by_structure(clean_doc_text, chunk_size)
    else:
        chunks = Chunker.fixed_size_chunking(clean_doc_text, chunk_size, overlap)

    bm25_search_obj = Retriever.create_search_engine(
        chunks,
        normalise_chunk_text=TextCleaner.normalise_chunk_text,
        tokenize_text=tokenize_normalised_text,
    )

    for question in user_questions:
        try:
            clean_question = TextCleaner.normalise_text(question)
            tokenized_question = tokenize_normalised_text(clean_question)
            best_chunk = Retriever.find_chunk(tokenized_question, chunks, bm25_search_obj)
            if not best_chunk:
                print("Information provided doesn't have relevant context")
                continue

            answer = ask_model(question, best_chunk, max_tokens, config=Config())
            print(f"Response: {answer}")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
