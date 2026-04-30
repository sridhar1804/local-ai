"""Entry point — canonical control flow for Phase 1.

Parses the query from argv, composes router → agent → trace, prints the output,
and writes one JSONL trace. Failed calls still produce a trace with error data.
"""

from __future__ import annotations

import logging
import sys

from agents.main_agent import run as agent_run
from agents.router import route as router_route
from model_memory.sink import JsonlTraceSink
from model_memory.trace import GenerationRecord, Trace
from models.client import Phi3Client

_logger = logging.getLogger(__name__)


def handle(query: str, client: Phi3Client, sink: JsonlTraceSink) -> str:
    """Compose the router, agent, and trace into the canonical control flow.

    On success the model completion is returned. On failure the exception
    is captured into the trace (written in finally) and re-raised.

    Args:
        query: The user's input query.
        client: An initialized Phi3Client for model calls.
        sink: A TraceSink for persisting the trace.

    Returns:
        The model's completion string.

    Raises:
        ValueError: If the router returns an unknown route.
        Exception: Any exception from the agent or model call is re-raised.
    """
    trace = Trace(input_query=query)
    output: str

    try:
        trace.decision_path.append("router.route")
        decision = router_route(query)
        trace.route = decision.route
        trace.decision_path.append(f"router→{decision.route}")

        if decision.route == "main_agent":
            trace.decision_path.append("main_agent.run")
            result = agent_run(query, client)
            trace.generation = GenerationRecord(
                model=result.generation.model,
                prompt=result.assembled_prompt,
                completion=result.generation.completion,
                prompt_tokens=result.generation.prompt_tokens,
                completion_tokens=result.generation.completion_tokens,
                latency_ms=result.generation.latency_ms,
                sampling=result.generation.sampling,
            )
            trace.final_output = result.output
            trace.decision_path.append("done")
            output = result.output
        else:
            raise ValueError(f"Unknown route: {decision.route}")
    except Exception as exc:
        _logger.error("Request failed", exc_info=True)
        trace.capture_exception(exc)
        trace.decision_path.append("error")
        raise
    else:
        _logger.info("Request completed", extra={"trace_id": trace.trace_id})
    finally:
        sink.write(trace)

    return output


def main() -> None:
    """Parse CLI arguments and run the agent pipeline.

    Prints the completion to stdout on success, writes a trace regardless.
    Exits with code 2 if no query is provided.
    """
    if len(sys.argv) < 2:
        _logger.warning("Usage: python -m main <query>")
        sys.exit(2)

    query = " ".join(sys.argv[1:])
    client = Phi3Client()
    sink = JsonlTraceSink()

    try:
        output = handle(query, client, sink)
        print(output)
    finally:
        client.close()


if __name__ == "__main__":
    main()
