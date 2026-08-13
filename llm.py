import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

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
