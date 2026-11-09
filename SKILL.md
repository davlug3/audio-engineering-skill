---
name: audio-engineering-skill
description: Design and specify audio circuits and systems from sourced engineering evidence. Use for microphone preamps, line and phono stages, headphone and power amplifiers, guitar pedals, crossovers, audio power supplies, grounding and shielding, loudspeakers, room acoustics, psychoacoustics, audio measurement, and music/sound-engineering standards. Covers audio analog circuit design, power-supply design, gain/noise/headroom budgets, and a versioned handoff to circuit-design-skill for simulation, schematic generation and verification.
license: MIT
---

# Audio Engineering

Design audio equipment the way an audio engineer does: establish the signal
chain and its levels, set the budgets, choose a topology from sourced practice,
then hand the electrical implementation to `circuit-design-skill` for
simulation, drawings and verification.

This skill is the audio domain layer. It does **not** reimplement SPICE, MNA,
KiCad generation or model management. It decides what an audio circuit must do,
why, and how its performance will be judged.

## Non-negotiables

1. **Research before you answer.** Never supply an audio-circuitry value,
   topology, part number, pinout, limit, formula, standard or failure mode from
   model memory. Recall may generate hypotheses and search queries; it is not
   evidence. Open the source during this session. If browsing is unavailable,
   stop and produce a research plan: the question list, the exact sources and
   queries to try, what is already verified and what remains unverified. See
   `references/research-protocol.md` §8.
2. **No number without a source.** Every numeric claim carries a citation that
   resolves in `catalog/sources.json`. If no verified source exists, write
   "unverified" and record the gap in `references/source-gaps.md`.
3. **Separate evidence from hypothesis.** Label anything not traced to a source
   as a hypothesis, and say what test would settle it.
4. **State the conditions.** A THD, noise, bandwidth or SPL number is
   meaningless without level, frequency, load, bandwidth, weighting and
   measurement method.
5. **Cite only what you opened.** Do not cite search snippets, summaries,
   aggregator pages or an AI answer. Record the locator (section, page, clause,
   figure) and the access date.
6. **Do not duplicate the electrical engine.** Component sizing, netlists,
   MNA, ngspice and KiCad belong to `circuit-design-skill`. Hand off; do not
   copy its code or conclusions.
7. **Simulation is not measurement.** Never claim a simulated result proves
   sound, reliability or a clone. Say what was simulated, with which models,
   and what remains unmeasured.
8. **Record gaps and conflicts.** Unsupported areas and contradictory sources
   are listed, not averaged away or hidden.
9. **Respect access and licensing.** Link and cite paywalled papers and
   restricted vendor material. Do not mirror PDFs, artwork or proprietary
   models.
10. **Escalate safety.** Mains wiring, phantom power, valve voltages, thermal
    and lithium cells need explicit safety review. Do not present a
    mains-connected design as ready without that review.

## Scope

This skill owns:

- audio signal chain, levels, impedance, balancing and gain staging;
- audio analog design: microphone preamps, line and phono stages, buffers,
  filters/EQ, headphone amplifiers, power amplifiers, pedals and crossovers;
- audio power supplies: transformers and rectifiers, reservoir and ripple,
  linear regulators and LDOs, capacitance multipliers, CRC/CLC filters,
  switching supplies, PSRR, decoupling, phantom and heater supplies, inrush,
  fusing and grounding;
- transducers, loudspeakers, room acoustics and psychoacoustics;
- audio measurement and listening-test methodology, including loudness
  standards;
- bounded music/sound-engineering workflow material, labelled subjective where
  it is taste rather than engineering.

It does not own:

- SPICE netlists, MNA solving, LTspice/KiCad files, footprint/pin mapping;
- PCB layout, DRC, DFM or fabrication;
- vendor model licensing or redistribution;
- claims of measured performance without a measurement.

## Workflow

### 0. Intake

Establish the application, source and load, levels, bandwidth, distortion and
noise targets, power available, environment, cost and safety class. Use
`templates/audio-requirements.md`. If the user cannot answer, propose a default,
cite the basis and record it as an assumption.

**Defaults confirmation gate (required before generating artifacts):** when the
user gives an ambiguous answer (e.g. “yes/proceed/use defaults”), restate the
locked defaults and assumptions explicitly and get a clear confirmation (for
example: `defaults confirmed` or a list of changes). Do not silently lock
revision/topology, power, bypass, build form factor, or anchor sources.

**Using in a target project (external repo):** the skill’s own
`catalog/sources.json`/`evidence/` are examples, not the project’s registry.
Bootstrap project-local evidence with:

```bash
python3 <audio-engineering-skill>/scripts/init_project_audio_evidence.py --out <project>/audio-evidence
python3 <audio-engineering-skill>/scripts/source_check.py --strict \
  --catalog <project>/audio-evidence/catalog/sources.json \
  --evidence-dir <project>/audio-evidence/evidence \
  --handoff <project>/audio-evidence/handoff.json
```

### 1. Research

For each question, search the source hierarchy in
`references/research-protocol.md`, open the sources, and write claims to
`evidence/<topic>.jsonl` before writing prose. Every claim records value,
conditions, source id and locator.

### 2. Architecture and budgets

Choose the block diagram and write the stage-by-stage budgets:

- gain distribution and headroom;
- noise contribution, referred to the input;
- impedance and loading;
- bandwidth and slew rate;
- distortion budget;
- power, thermal and supply rejection.

Use `templates/stage-budget.md` and `templates/psu-budget.md`. Use
`references/analog-design.md` for the noise, op-amp, distortion and output-stage
method, `references/power-amplifiers.md` for the load, thermal, SOA and
protection budgets, and `references/power-supplies.md` for the supply budget
and regulator choices.

### 3. Topology and parts

Choose the topology and candidate parts from sourced practice, not memory. A
part choice needs a datasheet, an operating point, alternatives and residual
risk. Record it in `templates/decision-record.md`, including the claim IDs, the
conditions and any perceptual hypothesis.

### 4. Handoff

Emit a `handoff.json` (schema in `references/handoff.md`) containing
requirements, conditions, target metrics and sources. Validate it with
`python3 scripts/source_check.py --strict --handoff handoff.json`; the checker
requires every requirement source to be verified and listed, and every metric
to use a supported measure and reference an existing requirement.
`examples/mic-preamp-handoff.json` is a complete example.
`circuit-design-skill` merges the handoff into a design spec, sizes
components, simulates and verifies.

### 5. Measurement plan

Write the bench and listening plan before building: instruments, fixtures,
levels, bandwidth, weighting, number of units, acceptance limits and what will
be recorded. Use `templates/measurement-plan.md` and
`templates/listening-test.md`. Simulation can only pre-screen.

### 6. Review

Check every claim for a source, every target for conditions, and every gap for
an explicit statement. Run `scripts/source_check.py --strict` before
publishing.

## Research and sources

- `references/research-protocol.md` — triggers, search order, evidence rules,
  conflict handling and the required answer format.
- `references/source-policy.md` — source tiers, registry schema, inclusion and
  exclusion, access and licensing, maintenance.
- `catalog/sources.json` — the registry. Only `verified` entries may be cited.
- `evidence/` — claim records, one JSON object per line.
- `references/source-gaps.md` — known unsupported areas.

A source is not "reliable" because it is popular or recent. It is reliable
because of its provenance, method and traceability.

## Knowledge documents

These are written from the claims in `evidence/` and each carries a
`## Sources` section:

- `references/analog-design.md` — noise, op-amp selection, distortion
  mechanisms, output stages and a microphone-preamplifier case study.
- `references/small-signal-audio.md` — levels, impedance, gain distribution,
  buffers, balanced and unbalanced interfaces, input protection, RF immunity
  and tone controls.
- `references/power-amplifiers.md` — load envelope, output-stage choice,
  thermal chain, SOA and derating, short-circuit and speaker protection,
  reactive loads and Class-D thermal notes.
- `references/power-supplies.md` — transformer, rectifier and reservoir
  sizing, LM317/LDO regulators, capacitance multipliers, PSRR, fusing, inrush
  and supply layout.
- `references/grounding-shielding.md` — safety earth, ground loops, balanced
  interfaces, the pin 1 problem, star versus mesh, and the loop breaker.
- `references/measurement.md` — THD, THD+N, IMD, S/N, EIN, CMRR, crosstalk,
  maximum levels and BS.1770 loudness.

Planned but not yet written: `audio-topologies.md`, `acoustics.md`,
`psychoacoustics.md`, `production.md`. Their open questions and the coverage
that already exists are tracked in `references/content-plan.md`.

## Handoff to circuit-design-skill

`references/handoff.md` defines contract version 1. The short form:

```json
{
  "handoff_version": 1,
  "application": "microphone preamplifier",
  "conditions": {"input_vrms": 0.002, "frequency_hz": 1000, "load_ohm": 10000},
  "requirements": [
    {"id": "A1", "text": "Flat gain, 40 dB", "acceptance": "40 +/-0.5 dB, 20 Hz-20 kHz", "source": "S041"}
  ],
  "metrics": [
    {"measure": "gain_db", "target": 40.0, "tolerance": 0.5, "requirement": "A1"}
  ],
  "sources": [{"id": "S041", "title": "RaneNote 145: Audio Specifications"}]
}
```

The circuit skill owns the electrical truth: netlist, simulation and drawings.
This skill owns the audio targets and their justification.

## Repository map

```
SKILL.md                  this file
README.md                 overview and quick start
references/               scope, research, sources, handoff, knowledge documents
catalog/sources.json      verified and candidate sources
evidence/                 claim records (JSONL)
templates/                requirements, budgets, decision record, measurement, handoff
examples/                 complete handoff example
scripts/source_check.py   registry/evidence/citation/handoff linter
scripts/check_links.py    link and URL checker
tests/                    unit tests
```

## Limits

- The skill can require research, but it cannot force a harness without web
  tools to browse. When browsing is unavailable, answers must say so.
- Audio circuit knowledge moves: datasheets are revised, parts go obsolete and
  standards get new editions. Treat the registry as a living artifact.
- Practical audio claims are often conditional. Prefer a measured result with
  stated conditions over a rule of thumb.
