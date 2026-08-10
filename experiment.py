import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from ingest import load_text, chunk_text
from text_utils import clean_words

def load_questions() -> list[str]:
    questions = ["whats chunking?", "what is fixed-size chunking?", "what are the drawbacks of fixed-size chunking?"]

    return questions

def find_relevant_chunk(question: str, chunks: list[str]) -> tuple[int, str, dict[str, int]]:
    if not chunks:
        return 0, "", {}

    question_words = clean_words(question)
    
    best_chunk = ""
    best_score = 0
    matched_words = {}

    for chunk in chunks:
        chunk_word_list = clean_words(chunk)
        chunk_word_set  = set(chunk_word_list)

        matched = {word: chunk_word_list.count(word) for word in question_words if word in chunk_word_set}
        score = len(matched)

        if score > best_score:
            best_score = score
            matched_words = matched
            best_chunk = chunk

    if best_score == 0:
        return 0, "", {}

    return best_score, best_chunk, matched_words

def ask_model(question: str, context: str, max_tokens: int, client: OpenAI) -> str:
    messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content":"Answer using only the context provided. Do not use outside knowledge. Respond in the same language as the question."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"
        }
    ]
    try:
        response = client.chat.completions.create(
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.5
        )
    
        answer = response.choices[0].message.content
        if answer is None:
            return "I couldn't generate a response."

        if answer.strip() == "":
            return "The model returned an empty response."

        return answer
    
    except Exception as e:
        print(f"Error while asking model: {str(e)}")
        return "Error while asking model."

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
        base_url="https://api.deepseek.com",
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )

    for question in load_questions():
        score, context, matched_words = find_relevant_chunk(question, chunks)

        context_preview = context[:50] + "..." if context else "No context available."
        context_index = chunks.index(context) if context and  context in chunks else -1

        print(f"\n\n[question]: \n{question}\n[Best chunk]:\n{context_preview}\n[chunk index]: #{context_index}\n[matched words]: {matched_words}\n[Score]: {score}\n")

        if score == 0:
            answer = "No relevant context found for the question."
        else:
            answer = ask_model(question, context, max_tokens, client)

        print(f"[Answer]:\n {answer}\n\n")


if __name__ == "__main__":
    main()
