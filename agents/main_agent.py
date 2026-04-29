"""Main agent — the only handler in Phase 1."""

from __future__ import annotations

from dataclasses import dataclass

from models.client import GenerationResult, Phi3Client

SYSTEM_PROMPT = (
    "You are a helpful, accurate, and concise AI assistant. "
    "Answer the user's question directly and clearly. "
    "If you are unsure, say so rather than guessing."
)


@dataclass
class AgentResult:
    output: str
    assembled_prompt: str
    generation: GenerationResult


def run(query: str, client: Phi3Client) -> AgentResult:
    assembled = f"<system>{SYSTEM_PROMPT}</system>\n<user>{query}</user>"
    gen = client.generate(user_message=query, system_message=SYSTEM_PROMPT)
    return AgentResult(output=gen.completion, assembled_prompt=assembled, generation=gen)
