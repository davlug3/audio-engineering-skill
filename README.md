# Audio Engineering Skill

Audio and sound-engineering knowledge for designing audio circuits and systems
from **sourced evidence** — not from model memory.

This is the domain layer above [`circuit-design-skill`](https://github.com/davlug3/circuit-design-skill).
It sets audio requirements, levels, budgets, topology and target performance,
then hands the electrical implementation to the circuit skill for SPICE,
schematics, KiCad and verification.

## What it covers

- audio signal chain, levels, impedance, balancing and gain staging;
- microphone preamps, line and phono stages, buffers, filters/EQ, headphone
  and power amplifiers, guitar pedals, crossovers;
- audio power supplies: linear/LDO, capacitance multipliers, CRC/CLC,
  switching supplies, PSRR, decoupling, phantom and heater supplies, inrush,
  fusing, grounding and shielding;
- loudspeakers, rooms, psychoacoustics and loudness standards;
- audio measurement and listening-test methodology;
- bounded music/sound-engineering workflow material.

## What it does not do

- No SPICE netlist, MNA, LTspice or KiCad generation — use the circuit skill.
- No PCB layout, DRC/DFM or fabrication — use `pcb-design-skill`.
- No claim that a simulation sounds like a reference device.
- No mirrored paywalled papers or restricted vendor models.

## Research-first rule

Every value, limit, formula, topology, part, pinout and standard must be traced
to a source opened in the current session. Answers carry a **Sources** section
and label anything unverified as a hypothesis. See
[`references/research-protocol.md`](references/research-protocol.md).

## Source registry

[`catalog/sources.json`](catalog/sources.json) holds the registry. Each entry
records tier, provenance, access status and access date. Only `verified`
entries may be cited. Claims live in [`evidence/`](evidence/) as JSONL records
linked to a source id and locator.

Known unsupported areas are listed in
[`references/source-gaps.md`](references/source-gaps.md) rather than hidden.

## Quick start

1. Read the intake questions in [`templates/audio-requirements.md`](templates/audio-requirements.md).
2. Research and record claims in `evidence/`.
3. Write the architecture and budgets with
   [`templates/stage-budget.md`](templates/stage-budget.md) and
   [`templates/psu-budget.md`](templates/psu-budget.md).
4. Emit a handoff per [`references/handoff.md`](references/handoff.md).
5. Run `python3 scripts/source_check.py` before publishing.
6. Hand the handoff to `circuit-design-skill` for simulation and drawings.

## Repository layout

```
SKILL.md                  agent instructions
references/               scope, research, sources, handoff, curricula
catalog/sources.json      source registry
evidence/                 claim records (JSONL)
templates/                requirements, budgets, measurement, handoff
scripts/source_check.py   registry/evidence/citation linter
tests/                    unit tests
.github/workflows/ci.yml  CI
```

## Status

This repository is being built evidence-first. Governance, the registry and the
handoff contract are in place; the analog, power-supply, acoustics and
measurement references are added as their evidence records are completed. See
[`references/content-plan.md`](references/content-plan.md) for the roadmap and
what is currently written.

## Related skills

- [`circuit-design-skill`](https://github.com/davlug3/circuit-design-skill) —
  electrical design, SPICE, KiCad, verification.
- [`pcb-design-skill`](https://github.com/davlug3/pcb-design-skill) — layout,
  DRC/DFM, fabrication outputs.

## License

MIT. Paywalled and restricted sources are linked and cited, never
redistributed.
