"""Tests for the registry, evidence and citation linter."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from source_check import check  # noqa: E402


def make_source(**overrides):
    source = {
        "id": "S001",
        "tier": 1,
        "title": "Test standard",
        "authors": ["Test Body"],
        "year": 2023,
        "venue": "Test Venue",
        "doi": None,
        "url": "https://example.invalid/standard",
        "accessed": "2026-11-08",
        "status": "verified",
        "access": "open",
        "topics": ["measurement"],
        "note": "",
    }
    source.update(overrides)
    return source


class Repo:
    def __init__(self, sources=None):
        self.dir = tempfile.TemporaryDirectory()
        self.root = Path(self.dir.name)
        (self.root / "catalog").mkdir()
        (self.root / "references").mkdir()
        (self.root / "evidence").mkdir()
        self.write_registry(sources if sources is not None else [make_source()])

    def write_registry(self, sources):
        payload = {"schema_version": 1, "updated": "2026-11-08", "sources": sources}
        (self.root / "catalog" / "sources.json").write_text(
            json.dumps(payload), encoding="utf-8")

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def cleanup(self):
        self.dir.cleanup()


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.cleanup()

    def test_valid_registry_passes(self):
        self.repo.write("references/topic.md",
                        "# Topic\n\nA claim [S001].\n\n## Sources\n- [S001] Test.\n")
        result = check(self.repo.root)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["counts"]["verified"], 1)

    def test_duplicate_id_fails(self):
        self.repo.write_registry([make_source(), make_source()])
        result = check(self.repo.root)
        self.assertFalse(result["ok"])
        self.assertTrue(any("duplicate id" in e for e in result["errors"]))

    def test_unknown_citation_fails(self):
        self.repo.write("references/topic.md",
                        "# Topic\n\nClaim [S009].\n\n## Sources\n- none\n")
        result = check(self.repo.root)
        self.assertFalse(result["ok"])
        self.assertTrue(any("unknown source S009" in e for e in result["errors"]))

    def test_candidate_cannot_be_cited(self):
        self.repo.write_registry([make_source(status="candidate", accessed=None)])
        self.repo.write("references/topic.md",
                        "# Topic\n\nClaim [S001].\n\n## Sources\n- none\n")
        result = check(self.repo.root)
        self.assertFalse(result["ok"])
        self.assertTrue(any("not verified" in e for e in result["errors"]))

    def test_malformed_source_fails(self):
        self.repo.write_registry([make_source(tier=9)])
        result = check(self.repo.root)
        self.assertFalse(result["ok"])


class TestEvidence(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.cleanup()

    def claim(self, **overrides):
        claim = {
            "id": "C001",
            "statement": "A measured value",
            "value": 1.0,
            "unit": "V",
            "conditions": "1 kHz",
            "source": "S001",
            "locator": "p. 1",
            "confidence": "high",
            "checked": "2026-11-08",
        }
        claim.update(overrides)
        return claim

    def test_valid_claim_passes(self):
        self.repo.write("evidence/topic.jsonl", json.dumps(self.claim()) + "\n")
        self.repo.write("references/topic.md",
                        "# Topic\n\nClaim [C001].\n\n## Sources\n- [S001] Test.\n")
        result = check(self.repo.root)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["counts"]["claims"], 1)

    def test_unknown_source_fails(self):
        self.repo.write("evidence/topic.jsonl",
                        json.dumps(self.claim(source="S099")) + "\n")
        result = check(self.repo.root)
        self.assertFalse(result["ok"])
        self.assertTrue(any("unknown source" in e for e in result["errors"]))

    def test_claim_needs_locator(self):
        self.repo.write("evidence/topic.jsonl",
                        json.dumps(self.claim(locator="")) + "\n")
        result = check(self.repo.root)
        self.assertFalse(result["ok"])

    def test_malformed_jsonl_fails(self):
        self.repo.write("evidence/topic.jsonl", "{not json}\n")
        result = check(self.repo.root)
        self.assertFalse(result["ok"])

    def test_duplicate_claim_fails(self):
        line = json.dumps(self.claim()) + "\n"
        self.repo.write("evidence/topic.jsonl", line + line)
        result = check(self.repo.root)
        self.assertFalse(result["ok"])


class TestDocs(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.cleanup()

    def test_knowledge_doc_without_sources_fails_strict(self):
        self.repo.write("references/topic.md", "# Topic\n\nUnsupported prose.\n")
        result = check(self.repo.root, strict=True)
        self.assertFalse(result["ok"])
        self.assertTrue(any("Sources" in e for e in result["errors"]))

    def test_knowledge_doc_without_sources_warns_non_strict(self):
        self.repo.write("references/topic.md", "# Topic\n\nUnsupported prose.\n")
        result = check(self.repo.root, strict=False)
        self.assertTrue(result["ok"])
        self.assertTrue(any("Sources" in w for w in result["warnings"]))

    def test_governance_doc_is_exempt(self):
        self.repo.write("references/scope.md", "# Scope\n\nNo citations needed.\n")
        result = check(self.repo.root, strict=True)
        self.assertTrue(result["ok"], result["errors"])

    def test_fenced_example_is_not_linted(self):
        self.repo.write("references/topic.md",
                        "# Topic\n\nClaim [S001].\n\n"
                        "```json\n[{\"source\": \"S999\"}]\n```\n\n"
                        "## Sources\n- [S001] Test.\n")
        result = check(self.repo.root)
        self.assertTrue(result["ok"], result["errors"])

    def test_inline_code_is_not_linted(self):
        self.repo.write("references/topic.md",
                        "# Topic\n\nCite `[S999]` as an example. Real [S001].\n\n"
                        "## Sources\n- [S001] Test.\n")
        result = check(self.repo.root)
        self.assertTrue(result["ok"], result["errors"])


class TestHandoff(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def tearDown(self):
        self.repo.cleanup()

    def handoff(self, **overrides):
        payload = {
            "handoff_version": 1,
            "application": "test preamplifier",
            "conditions": {
                "input_vrms": 0.002,
                "frequency_hz": 1000,
                "load_ohm": 10000,
            },
            "requirements": [
                {
                    "id": "A1",
                    "text": "Flat gain",
                    "acceptance": "40 +/-0.5 dB, 20 Hz-20 kHz",
                    "source": "S001",
                }
            ],
            "metrics": [
                {
                    "measure": "gain_db",
                    "target": 40.0,
                    "tolerance": 0.5,
                    "requirement": "A1",
                }
            ],
            "sources": [
                {
                    "id": "S001",
                    "title": "Test standard",
                    "url": "https://example.invalid/standard",
                    "accessed": "2026-11-08",
                }
            ],
        }
        payload.update(overrides)
        return payload

    def validate(self, payload):
        path = self.repo.root / "handoff.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return check(self.repo.root, handoffs=[str(path)])

    def test_valid_handoff_passes(self):
        result = self.validate(self.handoff())
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["counts"]["handoffs_checked"], 1)

    def test_limit_metric_without_tolerance_passes(self):
        payload = self.handoff()
        payload["metrics"] = [
            {"measure": "ein_uv", "max": 1.0, "requirement": "A1"}
        ]
        result = self.validate(payload)
        self.assertTrue(result["ok"], result["errors"])

    def test_exploratory_metric_without_requirement_passes(self):
        payload = self.handoff()
        payload["metrics"] = [
            {"measure": "thd_percent", "max": 0.01, "exploratory": True}
        ]
        result = self.validate(payload)
        self.assertTrue(result["ok"], result["errors"])

    def test_supported_measures_pass(self):
        measures = (
            "gain_db",
            "bandwidth_hz",
            "bandwidth_low_hz",
            "bandwidth_width_hz",
            "thd_percent",
            "ein_uv",
            "noise_uv",
            "output_vrms",
        )
        for measure in measures:
            with self.subTest(measure=measure):
                payload = self.handoff()
                payload["metrics"] = [
                    {"measure": measure, "max": 1.0, "requirement": "A1"}
                ]
                result = self.validate(payload)
                self.assertTrue(result["ok"], result["errors"])

    def test_unsupported_measure_fails(self):
        payload = self.handoff()
        payload["metrics"] = [
            {"measure": "noise_uv_rms", "max": 1.0, "requirement": "A1"}
        ]
        result = self.validate(payload)
        self.assertFalse(result["ok"])
        self.assertTrue(any("unsupported measure" in e
                            for e in result["errors"]))

    def test_metric_without_target_or_limit_fails(self):
        payload = self.handoff()
        payload["metrics"] = [{"measure": "gain_db", "requirement": "A1"}]
        result = self.validate(payload)
        self.assertFalse(result["ok"])
        self.assertTrue(any("target+tolerance" in e for e in result["errors"]))

    def test_metric_without_requirement_fails(self):
        payload = self.handoff()
        payload["metrics"] = [
            {"measure": "gain_db", "target": 40.0, "tolerance": 0.5}
        ]
        result = self.validate(payload)
        self.assertFalse(result["ok"])
        self.assertTrue(any("requirement or exploratory" in e
                            for e in result["errors"]))

    def test_unknown_requirement_source_fails(self):
        payload = self.handoff()
        payload["requirements"][0]["source"] = "S099"
        payload["sources"][0]["id"] = "S099"
        result = self.validate(payload)
        self.assertFalse(result["ok"])
        self.assertTrue(any("unknown source S099" in e for e in result["errors"]))

    def test_candidate_source_fails(self):
        self.repo.write_registry([make_source(status="candidate", accessed=None)])
        result = self.validate(self.handoff())
        self.assertFalse(result["ok"])
        self.assertTrue(any("not verified" in e for e in result["errors"]))

    def test_metric_requirement_must_exist(self):
        payload = self.handoff()
        payload["metrics"][0]["requirement"] = "A9"
        result = self.validate(payload)
        self.assertFalse(result["ok"])
        self.assertTrue(any("A9" in e for e in result["errors"]))

    def test_requirement_source_must_be_listed(self):
        payload = self.handoff()
        payload["sources"] = []
        result = self.validate(payload)
        self.assertFalse(result["ok"])
        self.assertTrue(any("sources missing S001" in e for e in result["errors"]))

    def test_wrong_version_fails(self):
        payload = self.handoff(handoff_version=2)
        result = self.validate(payload)
        self.assertFalse(result["ok"])
        self.assertTrue(any("handoff_version" in e for e in result["errors"]))

    def test_duplicate_handoff_source_fails(self):
        payload = self.handoff()
        payload["sources"].append(dict(payload["sources"][0]))
        result = self.validate(payload)
        self.assertFalse(result["ok"])
        self.assertTrue(any("duplicate source id" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
