"""Main agent — the only handler in Phase 1.

Takes a query, calls the model, returns a result plus metadata.
No control flow logic — that lives in main.py.
"""

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
    """Output from a single agent run.

    Attributes:
        output: The model's completion text.
        assembled_prompt: Textual representation of the prompt sent to the model.
        generation: Raw GenerationResult from the client call.
    """

    output: str
    assembled_prompt: str
    generation: GenerationResult


def run(query: str, client: Phi3Client) -> AgentResult:
    """Execute the main agent: assemble prompt, call model, return result.

    Args:
        query: The user's input query.
        client: An initialized Phi3Client instance.

    Returns:
        AgentResult with the completion, assembled prompt, and raw generation data.
    """
    assembled = f"<system>{SYSTEM_PROMPT}</system>\n<user>{query}</user>"
    gen = client.generate(
        user_message=query,
        system_message=SYSTEM_PROMPT,
    )
    return AgentResult(
        output=gen.completion,
        assembled_prompt=assembled,
        generation=gen,
    )
