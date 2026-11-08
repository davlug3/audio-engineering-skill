#!/usr/bin/env python3
"""Probe registry URLs and report reachability.

Network access is required, so this is an opt-in CI job and a manual tool, not
part of the normal test suite. It does not modify the registry; use the report
to mark entries broken or superseded.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

USER_AGENT = "audio-engineering-skill-link-check/1.0"


def probe(url: str, timeout: float) -> dict[str, object]:
    request = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return {"url": url, "ok": True, "status": response.status}
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405):
            return probe_get(url, timeout)
        return {"url": url, "ok": False, "status": exc.code, "error": str(exc)}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"url": url, "ok": False, "status": None, "error": str(exc)}


def probe_get(url: str, timeout: float) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response.read(1)
            return {"url": url, "ok": True, "status": response.status}
    except urllib.error.HTTPError as exc:
        return {"url": url, "ok": False, "status": exc.code, "error": str(exc)}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"url": url, "ok": False, "status": None, "error": str(exc)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--all", action="store_true",
                        help="probe candidates too (default: verified only)")
    args = parser.parse_args(argv)

    registry = json.loads(
        (Path(args.root) / "catalog" / "sources.json").read_text(encoding="utf-8"))
    results: list[dict[str, object]] = []
    for source in registry.get("sources", []):
        if not args.all and source.get("status") != "verified":
            continue
        url = source.get("url")
        if not url:
            continue
        result = probe(url, args.timeout)
        result["id"] = source.get("id")
        result["title"] = source.get("title")
        results.append(result)

    failed = [result for result in results if not result["ok"]]
    if args.json:
        print(json.dumps({"results": results, "failed": len(failed)}, indent=2))
    else:
        for result in results:
            state = "ok" if result["ok"] else "FAIL"
            print(f"{state:4} {result.get('id')} {result.get('status')} "
                  f"{result['url']}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
