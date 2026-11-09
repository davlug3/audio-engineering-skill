#!/usr/bin/env python3
"""Bootstrap project-local audio evidence, registry and handoff scaffolding.

Creates a small directory tree for using the audio-engineering-skill evidence
workflow inside an external/target project, without modifying the skill's own
catalog. The generated registry contains only a placeholder candidate entry;
promote sources to verified (with opened URL, locator, accessed date, and
conditions recorded in evidence claims) before citing them.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REGISTRY_TEMPLATE = {
    "schema_version": 1,
    "updated": "YYYY-MM-DD",
    "policy": "Project-local registry. Only status=verified sources may be cited. "
              "See audio-engineering-skill references/source-policy.md.",
    "sources": [
        {
            "id": "S001",
            "tier": 1,
            "title": "REPLACE: primary source title",
            "authors": ["REPLACE"],
            "year": 2026,
            "venue": "REPLACE",
            "doi": None,
            "url": "https://example.invalid/replace-me",
            "accessed": None,
            "status": "candidate",
            "access": "open",
            "topics": ["REPLACE"],
            "note": "Candidate lead. Open the source, record accessed date/locator, "
                    "then set status=verified before citing.",
        }
    ],
}

HANDOFF_TEMPLATE = {
    "handoff_version": 1,
    "application": "REPLACE",
    "description": "Planning handoff; requirements/metrics must cite verified sources.",
    "conditions": {"frequency_hz": 1000},
    "architecture": {"summary": "REPLACE", "blocks": [], "supplies": []},
    "requirements": [
        {
            "id": "A1",
            "text": "REPLACE",
            "acceptance": "REPLACE with numeric limit and conditions",
            "source": "S001",
        }
    ],
    "metrics": [
        {
            "measure": "gain_db",
            "target": 0.0,
            "tolerance": 0.0,
            "requirement": "A1",
        }
    ],
    "risks": [],
    "sources": [
        {
            "id": "S001",
            "title": "REPLACE",
            "url": "https://example.invalid/replace-me",
            "accessed": "YYYY-MM-DD",
        }
    ],
}

GAPS_TEMPLATE = """# Source gaps

Record unsupported areas, conflicting sources, and candidate leads that are not
yet verified.

| Topic | Gap / conflict | Candidate source(s) | Test or source needed | Date |
|---|---|---|---|---|
| | | | | |
"""

EVIDENCE_README = """# Evidence claims (project-local)

One JSON object per line (`.jsonl`). Each claim must reference a verified source
in the project registry and include a locator and checked date.

Example:

```json
{"id":"C001","statement":"...","value":1.0,"unit":"V","conditions":"1 kHz, 10 kOhm load","source":"S001","locator":"datasheet p. 5, table 2","confidence":"high","checked":"YYYY-MM-DD"}
```
"""


def write(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"exists (use --force): {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="project-local audio evidence directory")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    parser.add_argument("--json", action="store_true", help="print created paths as JSON")
    args = parser.parse_args(argv)

    out = Path(args.out).resolve()
    created: list[str] = []
    files = {
        out / "catalog" / "sources.json": json.dumps(REGISTRY_TEMPLATE, indent=2) + "\n",
        out / "evidence" / "README.md": EVIDENCE_README,
        out / "evidence" / "claims.jsonl": "",
        out / "handoff.json": json.dumps(HANDOFF_TEMPLATE, indent=2) + "\n",
        out / "source-gaps.md": GAPS_TEMPLATE,
    }
    for path, text in files.items():
        write(path, text, args.force)
        created.append(str(path))

    if args.json:
        print(json.dumps({"ok": True, "created": created}, indent=2))
    else:
        print(f"created {len(created)} file(s) under {out}")
        print("next: open sources, promote registry entries to verified, record claims,")
        print("      then validate with:")
        print(f"  python3 <audio-engineering-skill>/scripts/source_check.py --strict \\")
        print(f"    --catalog {out / 'catalog/sources.json'} \\")
        print(f"    --evidence-dir {out / 'evidence'} \\")
        print(f"    --handoff {out / 'handoff.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
