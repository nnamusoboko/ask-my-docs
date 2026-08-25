import argparse
from typing import TypedDict
import logging

logger = logging.getLogger(__name__)

class CliArgs(TypedDict):
    file: str
    overlap: int
    chunk_size: int
    max_tokens: int
    chunker: str
    questions: list[str]


def get_cli_args() -> CliArgs:
    parser = argparse.ArgumentParser(description="Chunking quality experiment")

    _ = parser.add_argument("file", type=str, help="File with content to chunk")
    _ = parser.add_argument(
            "--questions",
            type=str,
            nargs="+",
            required=True,
            help="Enter question(s)"
        )
    _ = parser.add_argument("--overlap", type=int, default=50, help="overlap for chunks")
    _ = parser.add_argument("--chunk-size", type=int, default=500, help="window size")
    _ = parser.add_argument("--max-tokens", type=int, default=1000, help="maximum number of output tokens")
    _ = parser.add_argument("--chunker", type=str, choices=["fixed-size", "structured"], help="type of chunker to use")

    args = parser.parse_args()

    return CliArgs(
        file=args.file,
        overlap=args.overlap,
        chunk_size=args.chunk_size,
        max_tokens=args.max_tokens,
        chunker=args.chunker,
        questions=args.questions
    )
