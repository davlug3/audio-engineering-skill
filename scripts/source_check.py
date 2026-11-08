#!/usr/bin/env python3
"""Validate the source registry, evidence records, citation markers and handoffs.

Exit status is non-zero when the repository would publish an unsupported claim,
an unregistered citation, a malformed record, (with ``--strict``) a knowledge
document without a Sources section, or (with ``--handoff``) a handoff that
violates the contract or cites an unverified source.

Standard library only, so it runs anywhere the skill runs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
HANDOFF_VERSION = 1
SOURCE_ID_RE = re.compile(r"^S\d{3}$")
CLAIM_ID_RE = re.compile(r"^C\d{3}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CITE_RE = re.compile(r"\[([SC]\d{3})\]")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
SOURCES_HEADING_RE = re.compile(r"^##\s+Sources\s*$", re.IGNORECASE | re.MULTILINE)

SOURCE_STATUSES = {"verified", "candidate", "broken", "superseded"}
ACCESS_KINDS = {"open", "paywalled", "book"}
CONFIDENCE = {"high", "medium", "low"}

REQUIRED_SOURCE_FIELDS = (
    "id", "tier", "title", "authors", "year", "venue",
    "accessed", "status", "access", "topics",
)
REQUIRED_CLAIM_FIELDS = ("id", "statement", "source", "locator", "checked")

# Governance documents describe the process; they do not carry technical claims.
GOVERNANCE_DOCS = {
    "scope.md",
    "research-protocol.md",
    "source-policy.md",
    "handoff.md",
    "content-plan.md",
    "source-gaps.md",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_code(text: str) -> str:
    """Remove fenced blocks and inline code so examples are not linted."""
    kept: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            kept.append("")
            continue
        kept.append("" if in_fence else INLINE_CODE_RE.sub("", line))
    return "\n".join(kept)


def check_registry(root: Path) -> tuple[dict[str, dict[str, Any]], list[str], list[str]]:
    path = root / "catalog" / "sources.json"
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_file():
        return {}, [f"{path}: missing"], warnings
    try:
        data = read_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{path}: {exc}"], warnings

    if not isinstance(data, dict):
        return {}, [f"{path}: top level must be an object"], warnings
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{path}: schema_version must be {SCHEMA_VERSION}")
    sources = data.get("sources")
    if not isinstance(sources, list):
        return {}, [f"{path}: sources must be a list"], warnings

    by_id: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(sources):
        where = f"{path}: sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{where}: must be an object")
            continue
        missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in source]
        if missing:
            errors.append(f"{where}: missing {', '.join(missing)}")
            continue
        sid = source["id"]
        if not isinstance(sid, str) or not SOURCE_ID_RE.match(sid):
            errors.append(f"{where}: id must look like S001")
            continue
        if sid in by_id:
            errors.append(f"{where}: duplicate id {sid}")
            continue
        by_id[sid] = source

        if source["tier"] not in (1, 2, 3):
            errors.append(f"{where}: tier must be 1, 2 or 3")
        if not isinstance(source["title"], str) or not source["title"].strip():
            errors.append(f"{where}: title must be a non-empty string")
        authors = source["authors"]
        if not isinstance(authors, list) or not authors or not all(
                isinstance(a, str) and a.strip() for a in authors):
            errors.append(f"{where}: authors must be a non-empty list of strings")
        if not isinstance(source["year"], int):
            errors.append(f"{where}: year must be an integer")
        if not isinstance(source["venue"], str) or not source["venue"].strip():
            errors.append(f"{where}: venue must be a non-empty string")
        if source["status"] not in SOURCE_STATUSES:
            errors.append(f"{where}: status must be one of "
                          f"{', '.join(sorted(SOURCE_STATUSES))}")
        if source["access"] not in ACCESS_KINDS:
            errors.append(f"{where}: access must be one of "
                          f"{', '.join(sorted(ACCESS_KINDS))}")
        topics = source["topics"]
        if not isinstance(topics, list) or not topics or not all(
                isinstance(t, str) and t.strip() for t in topics):
            errors.append(f"{where}: topics must be a non-empty list of strings")

        url = source.get("url")
        doi = source.get("doi")
        if source["access"] == "book":
            if not url and not doi:
                pass  # books are cited by page, not URL
        elif not url and not doi:
            errors.append(f"{where}: needs url or doi (except books)")

        accessed = source["accessed"]
        if source["status"] == "verified":
            if not isinstance(accessed, str) or not DATE_RE.match(accessed):
                errors.append(f"{where}: verified source needs accessed=YYYY-MM-DD")
        elif accessed is not None and (
                not isinstance(accessed, str) or not DATE_RE.match(accessed)):
            errors.append(f"{where}: accessed must be YYYY-MM-DD or null")
        if source["status"] == "verified" and not url and source["access"] != "book":
            warnings.append(f"{where}: verified source has no url")

    return by_id, errors, warnings


def check_evidence(root: Path, sources: dict[str, dict[str, Any]]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    claims: set[str] = set()
    directory = root / "evidence"
    if not directory.is_dir():
        return claims, errors
    for path in sorted(directory.glob("*.jsonl")):
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            where = f"{path}:{lineno}"
            try:
                claim = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{where}: {exc}")
                continue
            if not isinstance(claim, dict):
                errors.append(f"{where}: must be a JSON object")
                continue
            missing = [field for field in REQUIRED_CLAIM_FIELDS if field not in claim]
            if missing:
                errors.append(f"{where}: missing {', '.join(missing)}")
                continue
            cid = claim["id"]
            if not isinstance(cid, str) or not CLAIM_ID_RE.match(cid):
                errors.append(f"{where}: id must look like C001")
                continue
            if cid in claims:
                errors.append(f"{where}: duplicate claim id {cid}")
                continue
            claims.add(cid)

            source_id = claim["source"]
            source = sources.get(source_id) if isinstance(source_id, str) else None
            if source is None:
                errors.append(f"{where}: unknown source {source_id!r}")
            elif source.get("status") != "verified":
                errors.append(f"{where}: source {source_id} is "
                              f"{source.get('status')!r}, not verified")
            if not isinstance(claim["locator"], str) or not claim["locator"].strip():
                errors.append(f"{where}: locator must be a non-empty string")
            if not isinstance(claim["checked"], str) or not DATE_RE.match(claim["checked"]):
                errors.append(f"{where}: checked must be YYYY-MM-DD")
            if "confidence" in claim and claim["confidence"] not in CONFIDENCE:
                errors.append(f"{where}: confidence must be high, medium or low")
            if "value" in claim and not isinstance(claim["value"], (int, float)):
                errors.append(f"{where}: value must be numeric when present")
    return claims, errors


def check_handoff(path: Path, sources: dict[str, dict[str, Any]]) -> list[str]:
    """Validate a handoff JSON file against the registry and its own ids.

    The handoff is the only contract between this skill and
    ``circuit-design-skill``.  A source id that is unregistered, unverified or
    absent from the handoff's own ``sources`` list is a broken contract.
    """
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: {exc}"]
    if not isinstance(data, dict):
        return [f"{path}: top level must be an object"]
    if data.get("handoff_version") != HANDOFF_VERSION:
        errors.append(f"{path}: handoff_version must be {HANDOFF_VERSION}")

    requirements = data.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        errors.append(f"{path}: requirements must be a non-empty list")
        requirements = []
    requirement_ids: set[str] = set()
    requirement_sources: set[str] = set()
    for index, requirement in enumerate(requirements):
        where = f"{path}: requirements[{index}]"
        if not isinstance(requirement, dict):
            errors.append(f"{where}: must be an object")
            continue
        rid = requirement.get("id")
        if not isinstance(rid, str) or not rid:
            errors.append(f"{where}: id must be a non-empty string")
        elif rid in requirement_ids:
            errors.append(f"{where}: duplicate requirement id {rid}")
        else:
            requirement_ids.add(rid)

        sid = requirement.get("source")
        if not isinstance(sid, str) or not SOURCE_ID_RE.match(sid):
            errors.append(f"{where}: source must look like S001")
            continue
        requirement_sources.add(sid)
        source = sources.get(sid)
        if source is None:
            errors.append(f"{where}: unknown source {sid}")
        elif source.get("status") != "verified":
            errors.append(
                f"{where}: source {sid} is {source.get('status')!r}, not verified")

    metrics = data.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        errors.append(f"{path}: metrics must be a non-empty list")
        metrics = []
    for index, metric in enumerate(metrics):
        where = f"{path}: metrics[{index}]"
        if not isinstance(metric, dict):
            errors.append(f"{where}: must be an object")
            continue
        measure = metric.get("measure")
        if not isinstance(measure, str) or not measure.strip():
            errors.append(f"{where}: measure must be a non-empty string")
        rid = metric.get("requirement")
        if rid is None:
            if not metric.get("exploratory"):
                errors.append(
                    f"{where}: needs a requirement or exploratory=true")
        elif not isinstance(rid, str) or rid not in requirement_ids:
            errors.append(
                f"{where}: requirement {rid!r} is absent from requirements")
        has_target = "target" in metric
        has_limit = "max" in metric or "min" in metric
        if not has_target and not has_limit:
            errors.append(f"{where}: needs target+tolerance, max or min")
        if has_target:
            if not isinstance(metric["target"], (int, float)):
                errors.append(f"{where}: target must be numeric")
            if "tolerance" not in metric:
                errors.append(f"{where}: target needs tolerance")
            elif not isinstance(metric["tolerance"], (int, float)):
                errors.append(f"{where}: tolerance must be numeric")
        for limit in ("max", "min"):
            if limit in metric and not isinstance(metric[limit], (int, float)):
                errors.append(f"{where}: {limit} must be numeric")

    listed = data.get("sources")
    if not isinstance(listed, list) or not listed:
        errors.append(f"{path}: sources must be a non-empty list")
        listed = []
    listed_ids: set[str] = set()
    for index, source in enumerate(listed):
        where = f"{path}: sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{where}: must be an object")
            continue
        sid = source.get("id")
        if not isinstance(sid, str) or not SOURCE_ID_RE.match(sid):
            errors.append(f"{where}: id must look like S001")
            continue
        if sid in listed_ids:
            errors.append(f"{where}: duplicate source id {sid}")
        else:
            listed_ids.add(sid)
        if not isinstance(source.get("title"), str) or not source["title"].strip():
            errors.append(f"{where}: title must be a non-empty string")
        accessed = source.get("accessed")
        if not isinstance(accessed, str) or not DATE_RE.match(accessed):
            errors.append(f"{where}: accessed must be YYYY-MM-DD")
        registry_source = sources.get(sid)
        if registry_source is None:
            errors.append(f"{where}: unknown source {sid}")
        elif registry_source.get("status") != "verified":
            errors.append(f"{where}: source {sid} is not verified")

    missing = requirement_sources - listed_ids
    if missing:
        errors.append(
            f"{path}: sources missing {', '.join(sorted(missing))}")
    return errors


def check_citations(root: Path, sources: dict[str, dict[str, Any]],
                    claims: set[str]) -> tuple[int, list[str]]:
    errors: list[str] = []
    scanned = 0
    for directory in (root / "references", root / "templates"):
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            scanned += 1
            text = strip_code(path.read_text(encoding="utf-8"))
            for lineno, line in enumerate(text.splitlines(), 1):
                for match in CITE_RE.finditer(line):
                    ident = match.group(1)
                    if ident.startswith("C"):
                        if ident not in claims:
                            errors.append(f"{path}:{lineno}: unknown claim {ident}")
                        continue
                    source = sources.get(ident)
                    if source is None:
                        errors.append(f"{path}:{lineno}: unknown source {ident}")
                    elif source.get("status") != "verified":
                        errors.append(
                            f"{path}:{lineno}: source {ident} is "
                            f"{source.get('status')!r}, not verified")
    return scanned, errors


def check_docs(root: Path, strict: bool) -> tuple[int, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    directory = root / "references"
    if not directory.is_dir():
        return 0, errors, warnings
    checked = 0
    for path in sorted(directory.glob("*.md")):
        if path.name in GOVERNANCE_DOCS:
            continue
        checked += 1
        text = strip_code(path.read_text(encoding="utf-8"))
        problem = None
        if not SOURCES_HEADING_RE.search(text):
            problem = "has no '## Sources' section"
        elif not CITE_RE.search(text):
            problem = "has no [C###] or [S###] citations"
        if problem:
            message = f"{path}: knowledge document {problem}"
            if strict:
                errors.append(message)
            else:
                warnings.append(message)
    return checked, errors, warnings


def check(root: Path, strict: bool = False,
          handoffs: list[str] | None = None) -> dict[str, Any]:
    sources, registry_errors, registry_warnings = check_registry(root)
    errors = list(registry_errors)
    warnings = list(registry_warnings)
    claims, evidence_errors = check_evidence(root, sources)
    errors.extend(evidence_errors)
    scanned, citation_errors = check_citations(root, sources, claims)
    errors.extend(citation_errors)
    docs, doc_errors, doc_warnings = check_docs(root, strict)
    errors.extend(doc_errors)
    warnings.extend(doc_warnings)
    handoff_paths = [Path(path) for path in handoffs or []]
    for path in handoff_paths:
        errors.extend(check_handoff(path, sources))
    return {
        "ok": not errors,
        "strict": strict,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "sources": len(sources),
            "verified": sum(1 for s in sources.values()
                            if s.get("status") == "verified"),
            "claims": len(claims),
            "documents_scanned": scanned,
            "knowledge_documents": docs,
            "handoffs_checked": len(handoff_paths),
        },
    }


def print_human(result: dict[str, Any]) -> None:
    counts = result["counts"]
    print(f"sources: {counts['sources']} "
          f"({counts['verified']} verified), claims: {counts['claims']}, "
          f"documents: {counts['documents_scanned']} scanned, "
          f"{counts['knowledge_documents']} knowledge, "
          f"handoffs: {counts['handoffs_checked']}")
    for warning in result["warnings"]:
        print(f"warning: {warning}")
    for error in result["errors"]:
        print(f"error: {error}")
    print("OK" if result["ok"] else f"FAILED ({len(result['errors'])} error(s))")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--strict", action="store_true",
                        help="treat missing Sources sections as errors")
    parser.add_argument("--handoff", action="append", default=[], metavar="PATH",
                        help="validate a handoff JSON file (repeatable)")
    args = parser.parse_args(argv)

    result = check(Path(args.root).resolve(), strict=args.strict,
                   handoffs=args.handoff)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
