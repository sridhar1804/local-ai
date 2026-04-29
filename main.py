"""Entry point — canonical control flow for Phase 1."""

from __future__ import annotations

import sys

from agents.main_agent import run as agent_run
from agents.router import route as router_route
from memory.sink import JsonlTraceSink
from memory.trace import GenerationRecord, Trace
from models.client import Phi3Client


def handle(query: str, client: Phi3Client, sink: JsonlTraceSink) -> str:
    trace = Trace(input_query=query)
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
            return result.output
        else:
            raise ValueError(f"Unknown route: {decision.route}")
    except Exception as exc:
        trace.capture_exception(exc)
        trace.decision_path.append("error")
        raise
    finally:
        sink.write(trace)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m main <query>", file=sys.stderr)
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
