#!/usr/bin/env python3
"""Graphical interaction UI for audio-engineering-skill (MVP).

Builds intake/defaults-confirm and handoff/plan review sessions using the
shared design-interact UI. Dependency-free; stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SHARED_SCRIPTS = SKILL_DIR.parent / "_shared" / "design-interact" / "scripts"
sys.path.insert(0, str(SHARED_SCRIPTS))

import design_interact as di  # noqa: E402


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_intake_payload(*, title: str | None = None) -> dict:
    return {
        "title": title or "Audio engineering requirements intake",
        "intro": "Provide audio requirements with conditions/sources where known. The agent will label unverified items and must get explicit confirmation before locking defaults/assumptions.",
        "skill": "audio-engineering-skill",
        "session_kind": "intake",
        "submit_label": "Send requirements",
        "blocks": [
            {"type": "preview", "title": "Defaults confirmation gate", "format": "markdown", "content":
             "State locked defaults and assumptions explicitly and get confirmation (`defaults confirmed` or a list of changes). "
             "Do not silently lock revision/topology, power, bypass, build form factor, anchor sources, or unverified substitutions."},
            {"type": "question", "id": "application", "question_type": "text", "required": True,
             "prompt": "Application, source, load, channels, environment, safety class?",
             "placeholder": "e.g., mic preamp, dynamic mic, 10k line load, mono, studio, SELV"},
            {"type": "question", "id": "revision_anchor", "question_type": "text", "required": False,
             "prompt": "If clone/variant: target revision/topology, primary anchor source, known conflicts, allowed substitutions (or N/A)."},
            {"type": "question", "id": "levels", "question_type": "text", "required": True,
             "prompt": "Levels/gain/headroom (nominal/max input & output, gain range)? Include conditions/sources if known."},
            {"type": "question", "id": "bandwidth_impedance", "question_type": "text", "required": True,
             "prompt": "Passband, input/output impedance, load range?"},
            {"type": "question", "id": "noise_distortion", "question_type": "text", "required": True,
             "prompt": "Noise/distortion/crosstalk targets with conditions (bandwidth, weighting, level, frequency, load, source Z, method)?"},
            {"type": "question", "id": "power_thermal", "question_type": "text", "required": True,
             "prompt": "Rails/current, PSRR target, ambient/cooling/thermal constraints?"},
            {"type": "question", "id": "acceptance", "question_type": "text", "required": False,
             "prompt": "Acceptance tests/methods and any verified sources/citations (IDs, links, datasheet refs) to anchor requirements."},
            {"type": "question", "id": "defaults_assumptions", "question_type": "text", "required": True,
             "prompt": "Defaults/assumptions to lock now. Reply with explicit confirmation text.",
             "placeholder": "defaults confirmed — OR list changes. Mark unverified items."},
            {"type": "review", "id": "requirements_review", "prompt": "Confirm requirements/defaults are sufficient for the agent to produce a handoff/spec plan.", "required": True,
             "decisions": [
                 {"id": "proceed", "label": "Proceed", "description": "Agent may draft handoff/budgets and state assumptions/gaps."},
                 {"id": "revise", "label": "Revise", "description": "I need to clarify targets, conditions, or defaults."},
                 {"id": "stop", "label": "Stop", "description": "Do not proceed."},
             ]},
        ],
    }


def _table_from(items, columns):
    if not isinstance(items, list):
        return {"columns": columns, "rows": []}
    rows = []
    for item in items:
        if not isinstance(item, dict):
            continue
        rows.append([json.dumps(item.get(c), ensure_ascii=False) if isinstance(item.get(c), (dict, list)) else str(item.get(c, "")) for c in columns])
    return {"columns": columns, "rows": rows}


def build_handoff_review_payload(*, handoff_path: Path, check_output: Path | None = None, title: str | None = None) -> dict:
    handoff = _load_json(handoff_path)
    blocks = []
    blocks.append({"type": "preview", "title": "Handoff summary", "format": "keyvalue", "content": {
        "handoff_version": handoff.get("handoff_version"),
        "application": handoff.get("application"),
        "conditions": json.dumps(handoff.get("conditions"), ensure_ascii=False),
        "requirements": len(handoff.get("requirements") or []),
        "metrics": len(handoff.get("metrics") or []),
        "sources": len(handoff.get("sources") or []),
    }})
    if handoff.get("requirements"):
        t = _table_from(handoff["requirements"], ["id", "text", "acceptance", "source"])
        blocks.append({"type": "preview", "title": "Requirements", "format": "table", **t})
    if handoff.get("metrics"):
        cols = ["id", "measure", "target", "tolerance", "min", "max", "output", "input", "requirement", "exploratory"]
        t = _table_from(handoff["metrics"], [c for c in cols if any(isinstance(m, dict) and c in m for m in handoff.get("metrics", []))] or ["measure", "output"])
        blocks.append({"type": "preview", "title": "Metrics", "format": "table", **t})
    if handoff.get("sources"):
        t = _table_from(handoff["sources"], ["id", "title", "status", "url", "accessed"])
        blocks.append({"type": "preview", "title": "Sources cited in handoff", "format": "table", **t,
                       "description": "Verify each source is registered/verified in the project's catalog before relying on it."})
    blocks.append({"type": "preview", "title": "Full handoff (JSON)", "format": "json", "path": str(handoff_path)})
    if check_output and check_output.is_file():
        suf = check_output.suffix.lower()
        fmt = "json" if suf == ".json" else "text"
        blocks.append({"type": "preview", "title": "Validation / source check output", "format": fmt, "path": str(check_output),
                       "description": "Precomputed check output provided to the review session."})
    else:
        blocks.append({"type": "preview", "title": "Validation note", "format": "markdown", "content":
                       "No precomputed check output was attached. For implementation-grade review, run `scripts/source_check.py --strict --handoff <handoff>` in the target project and attach the output with `--check-output`."})
    blocks.append({"type": "review", "id": "handoff_review", "required": True,
                   "prompt": f"Review audio handoff: {handoff.get('application') or handoff_path.name}",
                   "help": "Check conditions, source grounding, metrics/requirements linkage, and safety assumptions.",
                   "comment_label": "Feedback / requested changes"})
    return {
        "title": title or f"Audio handoff review: {handoff.get('application') or handoff_path.stem}",
        "intro": "MVP preview: handoff structure, requirements/metrics/sources tables, and optional validation output. Evidence quality depends on project-local catalog/evidence.",
        "skill": "audio-engineering-skill",
        "session_kind": "artifact-review",
        "artifacts_dir": str(handoff_path.parent.resolve()),
        "submit_label": "Send review",
        "blocks": blocks,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Graphical interaction UI for audio-engineering-skill.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_intake = sub.add_parser("intake")
    p_intake.add_argument("--out", required=True)
    p_intake.add_argument("--title")
    p_intake.add_argument("--host", default="127.0.0.1")
    p_intake.add_argument("--mobile", action="store_true")
    p_intake.add_argument("--port", type=int, default=8772)
    p_intake.add_argument("--timeout", type=float, default=1800)
    p_intake.add_argument("--detach", action="store_true")
    p_intake.add_argument("--open", action="store_true", dest="open_browser")
    p_intake.add_argument("--json", action="store_true", dest="print_json")

    p_rev = sub.add_parser("review-handoff")
    p_rev.add_argument("--handoff", required=True)
    p_rev.add_argument("--check-output")
    p_rev.add_argument("--out", required=True)
    p_rev.add_argument("--title")
    p_rev.add_argument("--host", default="127.0.0.1")
    p_rev.add_argument("--mobile", action="store_true")
    p_rev.add_argument("--port", type=int, default=8772)
    p_rev.add_argument("--timeout", type=float, default=1800)
    p_rev.add_argument("--detach", action="store_true")
    p_rev.add_argument("--open", action="store_true", dest="open_browser")
    p_rev.add_argument("--json", action="store_true", dest="print_json")

    args = parser.parse_args(argv)
    out_path = Path(args.out).expanduser().resolve()
    url_file = out_path.with_suffix(".url")
    status_file = out_path.with_suffix(".status.json")
    log_file = out_path.with_suffix(".log")
    host = "0.0.0.0" if args.mobile else args.host

    if args.command == "intake":
        payload = di.normalize_payload(build_intake_payload(title=args.title))
        artifacts_dir = None
    else:
        handoff_path = Path(args.handoff).expanduser().resolve()
        check_output = Path(args.check_output).expanduser().resolve() if args.check_output else None
        artifacts_dir = handoff_path.parent.resolve()
        payload = di.normalize_payload(build_handoff_review_payload(handoff_path=handoff_path, check_output=check_output, title=args.title), artifacts_dir=artifacts_dir)

    if args.detach:
        return di._detach(payload=payload, out_path=out_path, host=host, port=args.port, timeout=args.timeout,
                          url_file=url_file, status_file=status_file, log_file=log_file,
                          artifacts_dir=str(artifacts_dir) if artifacts_dir else None,
                          open_browser=args.open_browser, verbose=False)
    try:
        server = di.make_server(payload, out_path=out_path, host=host, port=args.port, status_path=status_file,
                                artifacts_dir=artifacts_dir)
    except OSError as exc:
        print(f"could not start interaction server: {exc}", file=sys.stderr)
        return 1
    return di.run_server(server, timeout=args.timeout, url_file=url_file, open_browser=args.open_browser, print_json=args.print_json)


if __name__ == "__main__":
    raise SystemExit(main())
