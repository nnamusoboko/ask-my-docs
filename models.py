from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    content:  str
    metadata: dict[str, str | int | float | None]
