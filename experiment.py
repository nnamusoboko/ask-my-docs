import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from ingest import load_text, chunk_text
from retrieval import find_relevant_chunk
from llm import ask_model

def load_questions() -> list[str]:
    questions = ["whats chunking?", "what is fixed-size chunking?", "what are the drawbacks of fixed-size chunking?"]

    return questions


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chunking quality experiment")
    
    parser.add_argument("file", type=str, help="File with content to chunk")
    parser.add_argument("--overlap", type=int, default=50, help="overlap for chunks")
    parser.add_argument("--chunk-size", type=int, default=500, help="window size")
    parser.add_argument("--max-tokens", type=int, default=300, help="maximum number of output tokens")
    
    args = parser.parse_args()

    file = args.file
    overlap = args.overlap
    chunk_size = args.chunk_size
    max_tokens = args.max_tokens

    text = load_text(file)
    chunks = chunk_text(text, chunk_size, overlap)

    client = OpenAI(
        base_url=os.getenv("MODEL_PROVIDER_BASE_URL"),
        api_key=os.getenv("MODEL_PROVIDER_API_KEY")
    )

    for question in load_questions():
        score, context, matched_words = find_relevant_chunk(question, chunks)

        context_preview = context[:50] + "..." if context else "No context available."
        context_index = chunks.index(context) if context and  context in chunks else -1

        print(f"\n\n[question]: \n{question}\n[Best chunk]:\n{context_preview}\n")
        print(f"[chunk index]: #{context_index}\n[matched words]: {matched_words}\n")
        print(f"[Score]: {score}\n[Model used]: {os.getenv("MODEL_NAME")}\n[Max-tokens-used]: {max_tokens}\n")

        if score == 0:
            answer = "No relevant context found for the question."
        else:
            answer = ask_model(question, context, max_tokens, client)

        print(f"[Answer]:\n {answer}\n\n")


if __name__ == "__main__":
    main()
