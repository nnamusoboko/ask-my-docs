import os
import argparse
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from ingest import load_text, chunk_text

def load_questions() -> list[str]:
    questions = []
    user_query = ""
    while user_query != "q":
        user_query = input("Ask your local document question(q--quit asking): ")
        if user_query != "q":
            questions.append(user_query)

    return questions

def find_relevant_chunk(question: str, chunks: list[str]) -> str:
    if not chunks:
        return ""

    question_words = question.lower().split()
    
    best_chunk = chunks[0]
    best_score = 0

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        score = sum(1 for word in question_words if word in chunk_words)
        if score > best_score:
            best_score = score
            best_chunk = chunk

    return best_chunk

def ask_model(question: str, context: str, client: OpenAI) -> str:
    messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content":"Answer using only the context provided. Do not use outside knowledge"},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"
        }
    ]
    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-ultra-550b-a55b:free",
            messages=messages,
            max_tokens=300,
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
    parser = argparse.ArgumentParser(description="Chunking quality experiment")
    
    parser.add_argument("file", type=str, help="File with content to chunk")
    parser.add_argument("--overlap", type=int, default=2, help="overlap for chunks")
    parser.add_argument("--chunk_size", type=int, default=4, help="window size")
    
    args = parser.parse_args()

    file = args.file
    overlap = args.overlap
    chunk_size = args.chunk_size

    text = load_text(file)
    chunks = chunk_text(text, chunk_size, overlap)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )

    for question in load_questions():
        context = find_relevant_chunk(question, chunks)
        answer = ask_model(question, context, client)

        print(f"Question: {question}\n\tAnswer: {answer}")


if __name__ == "__main__":
    main()
