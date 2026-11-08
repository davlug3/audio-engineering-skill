# Handoff to circuit-design-skill

Contract version: **1**.

This skill decides what the audio system must do. `circuit-design-skill` owns
the electrical implementation: component sizing, netlist, simulation,
schematic and verification.

## 1. Artifact

A single JSON file, conventionally `handoff.json`:

```json
{
  "handoff_version": 1,
  "application": "microphone preamplifier",
  "description": "Transformerless differential input, 40 dB gain",
  "conditions": {
    "input_vrms": 0.002,
    "frequency_hz": 1000,
    "load_ohm": 10000,
    "bandwidth_hz": [20, 20000],
    "temperature_c": 25
  },
  "architecture": {
    "summary": "differential input -> gain stage -> servo -> line driver",
    "blocks": ["input protection", "differential pair", "gain", "DC servo", "output"],
    "supplies": [{"name": "V+", "voltage": 15}, {"name": "V-", "voltage": -15}]
  },
  "requirements": [
    {
      "id": "A1",
      "text": "Flat gain within the audio band",
      "acceptance": "40 +/-0.5 dB, 20 Hz to 20 kHz, 10 kOhm load",
      "source": "S041"
    },
    {
      "id": "A2",
      "text": "Input-referred noise",
      "acceptance": "<= 1.0 uV RMS, 20 Hz to 20 kHz, 150 Ohm source",
      "source": "S045"
    }
  ],
  "metrics": [
    {"measure": "gain_db", "target": 40.0, "tolerance": 0.5, "requirement": "A1"},
    {"measure": "noise_uv_rms", "max": 1.0, "bandwidth_hz": [20, 20000], "requirement": "A2"},
    {"measure": "bandwidth_hz", "min": 20000, "passband": "low", "requirement": "A1"}
  ],
  "risks": [
    {"id": "R1", "risk": "RF rectification at the input", "mitigation": "input RC and common-mode choke", "verification": "bench RF injection"}
  ],
  "sources": [
    {"id": "S041", "title": "RaneNote 145: Audio Specifications", "url": "https://www.ranecommercial.com/legacy/note145.html", "accessed": "2026-11-08"},
    {"id": "S045", "title": "Noise in Audio Amplifiers", "url": "https://sound-au.com/noise.htm", "accessed": "2026-11-08"}
  ]
}
```

## 2. Field rules

- `handoff_version` is required and must be `1`.
- `application` and at least one requirement are required.
- Every requirement has `id`, `text`, `acceptance` and `source`.
- `source` must resolve to a registry entry in `catalog/sources.json` with
  status `verified`.
- Every metric either names a `requirement` or is marked
  `"exploratory": true`.
- A metric is either a target (`target` plus `tolerance`) or a limit (`max` or
  `min`).
- Numeric targets carry units in the field name or an explicit unit field.
- Conditions are mandatory: a target without conditions is rejected.
- Use SI units and RMS voltages unless stated otherwise.
- No part numbers in the handoff unless a datasheet source is recorded.

## 3. Merge into a circuit spec

The circuit skill maps:

| Handoff | Circuit spec |
|---|---|
| `requirements[]` | `design.requirements[]` |
| `conditions` | `metrics.conditions` (or the relevant analysis) |
| `metrics[]` | `metrics.metrics[]` |
| `architecture` | `design.architecture` |
| `risks[]` | `design.risks[]` |
| `sources[]` | `design.sources[]` |

The circuit skill must reject a metric whose `requirement` id is absent.

## 4. Validation

Before handoff:

1. `python3 scripts/source_check.py --strict --handoff <your-handoff.json>`
   passes. The ready example is `examples/mic-preamp-handoff.json`.
2. Every `source` id exists, is `verified` in `catalog/sources.json`, and is
   listed in the handoff's own `sources[]`.
3. Every metric references an existing requirement id.
4. Every metric has a condition and an acceptance limit.
5. Every requirement has a test method in the measurement plan.

## 5. Versioning

- Additive optional fields do not change the version.
- Renaming or removing a field, or changing units, requires a version bump.
- Both repos record the supported version. The circuit skill ignores unknown
  fields but rejects a higher major `handoff_version`.

## 6. What the handoff is not

- It is not a netlist, a schematic or a PCB.
- It is not a guarantee of measured performance.
- It does not transfer vendor model files or licensed documents.
