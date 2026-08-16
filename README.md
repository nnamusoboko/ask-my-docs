# Ask-my-docs

A tool that lets a user ask natural-language questions and get answers grounded in a
specific set of documents, instead of the model's general knowledge.

> **Status:** Under active development. Expect rough edges and changing behavior.

## Getting started

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install openai python-dotenv
   ```

3. Get an API key from any provider with an OpenAI-compatible API, for example [DeepSeek](https://platform.deepseek.com/api_keys) or [OpenRouter](https://openrouter.ai/workspaces/default/keys). Free-tier models work too, though quality varies.

4. Configure the environment:

   `cp .env.example .env`

   Fill in:

   - `MODEL_PROVIDER_API_KEY` — your provider's API key
   - `MODEL_NAME` — the model ID to use (e.g. `deepseek-v4-flash`)
   - `MODEL_PROVIDER_BASE_URL` — your provider's OpenAI-compatible endpoint.

## Usage

Put a text document in `data/`, then ask questions about it:

`python main.py data/sample.txt --chunk-size 500 --overlap 50`

Options:

- `--chunk-size` — chunk size in characters (default 500)
- `--overlap`    — overlap between chunks in characters (default 50)
- `--max-tokens` — maximum output tokens per answer (default 1000)

The script splits the document into overlapping chunks, finds the chunk most
relevant to each question using keyword matching, and answers using only that
chunk's text. Questions with no matching chunk are answered locally without a
model call.

## Files

- `ingest.py` — reads a text file and splits it into overlapping chunks
- `main.py` — asks questions about a document via an OpenAI-compatible API
- `llm.py` — forwards query to llm provider
- `retrieval.py` — finds chunks relevant to query
