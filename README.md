# Ask-my-docs

A tool that lets a user ask natural-language questions and get answers grounded in a specific set of documents, instead of the model's general knowledge.

## Getting started

1. Create and activate a virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate

2. Install the dependency:
   pip install openai

3. Get an API key at [OpenRouter keys](https://openrouter.ai/keys) and export it:
   export OPENROUTER_API_KEY=your_key_here

## Usage

Put a text document in `data/`, then ask questions about it:

**command:** `python experiment.py data/sample.txt --chunk_size 500 --overlap 50`

Options:

- `--chunk_size` — chunk size in characters (default 500)
- `--overlap` — overlap between chunks in characters (default 50)

The script splits the document into overlapping chunks, finds the chunk most relevant to each question, and answers using only that chunk's text.

## Files

- `ingest.py` — reads a text file and splits it into overlapping chunks
- `experiment.py` — asks questions about a document via OpenRouter
