import argparse
from pathlib import Path
from dotenv import load_dotenv

from agentic_platform.llm.ollama import OllamaLLM
from agentic_platform.agent.loop import AgentLoop
from agentic_platform.tracing import Tracer
from agentic_platform.utils.time import run_id
from agentic_platform.utils.json_io import write_json, write_jsonl

def main():
    load_dotenv()

    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--max-steps", type=int, default=8)
    args = ap.parse_args()

    tracer = Tracer()
    llm = OllamaLLM()
    agent = AgentLoop(llm=llm, tracer=tracer, max_steps=args.max_steps)

    final = agent.run(args.task)

    rid = run_id()
    out_dir = Path("outputs") / f"run_{rid}"
    out_dir.mkdir(parents=True, exist_ok=True)

    write_json(out_dir / "final.json", final)
    write_jsonl(out_dir / "trace.jsonl", tracer.events)

    print("\\n=== FINAL ===")
    print(final)
    print(f"\\nSaved outputs to: {out_dir}")

if __name__ == "__main__":
    main()
