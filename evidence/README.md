# Evidence Records

One JSON object per line (JSONL), grouped by topic:

```
evidence/analog-design.jsonl
evidence/small-signal.jsonl
evidence/power-amplifiers.jsonl
evidence/power-supplies.jsonl
evidence/grounding-shielding.jsonl
evidence/measurement.jsonl
```

Each record links a claim to a verified source and a locator.

```json
{"id": "C001", "statement": "The device is specified for a 10 kOhm load", "value": 10000, "unit": "ohm", "conditions": "Vs = +/-15 V, 1 kHz, 25 C", "source": "S004", "locator": "datasheet p. 5, table 2", "confidence": "high", "checked": "2026-11-08"}
```

## Required fields

| Field | Meaning |
|---|---|
| `id` | `C###`, unique across the repository |
| `statement` | The claim in one sentence |
| `source` | A registry id with status `verified` |
| `locator` | Section, page, clause, table or figure |
| `checked` | Date the source was opened, `YYYY-MM-DD` |

## Optional fields

`value`, `unit`, `conditions`, `confidence` (`high|medium|low`), `note`.

## Rules

- A claim without a verified source is a hypothesis; do not put it here as a
  fact.
- One claim per line; keep conditions with the value.
- Do not duplicate the same claim across files. Give it one id.
- If a source is later found wrong or superseded, mark the claim's source and
  revisit the documents that cite it.

`scripts/source_check.py` validates these records and the citations that point
at them.
