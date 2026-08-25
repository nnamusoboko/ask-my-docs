import logging
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from config import Config

logger = logging.getLogger(__name__)


def ask_model(question: str, context: str, max_tokens: int, config: Config) -> str:
    client = create_client(config.model_provider_base_url, config.model_provider_api_key)

    messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content":"Answer using only the context provided. Do not use outside knowledge. Respond in the same language as the question."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"
        }
    ]

    logger.info("Asking model (max %d tokens)", max_tokens)

    try:
        response = client.chat.completions.create(
            model=config.model_name,
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

def create_client(model_provider_base_url: str, model_provider_api_key: str) -> OpenAI:
    client = OpenAI(
        base_url=model_provider_base_url,
        api_key=model_provider_api_key
    )

    return client
