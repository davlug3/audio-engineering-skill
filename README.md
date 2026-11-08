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

The current verified base mixes standards, peer-reviewed work and practitioner
engineering:

- **Standards and regulators:** ITU-R BS.1770-5 for loudness and true peak;
  UL summaries of appliance leakage-current limits and Class A GFCI trip
  thresholds (summaries, not the standard text); IEC 60268-3 is referenced
  through the practical sources but is not yet in the registry as full text.
- **Peer-reviewed:** AES Convention Paper 8234 (Whitlock and Fox, 2010) on the
  magnetic-induction origin of ground voltage differences; *Journal of the
  Audio Engineering Society* 74(5) (Parolo, 2026) on distortion measurement.
- **Practitioner and manufacturer:** RaneNote 110 and 145, Douglas Self's
  distortion work, Elliott Sound Products, Texas Instruments application notes
  and the LM317 datasheet, THAT Corporation Design Note 140.

## Quick start

1. Read the intake questions in [`templates/audio-requirements.md`](templates/audio-requirements.md).
2. Read the relevant knowledge document:
   [`analog-design.md`](references/analog-design.md),
   [`power-supplies.md`](references/power-supplies.md),
   [`grounding-shielding.md`](references/grounding-shielding.md) or
   [`measurement.md`](references/measurement.md).
3. Research and record claims in `evidence/`.
4. Write the architecture and budgets with
   [`templates/stage-budget.md`](templates/stage-budget.md) and
   [`templates/psu-budget.md`](templates/psu-budget.md).
5. Emit a handoff per [`references/handoff.md`](references/handoff.md).
6. Validate the handoff with
   `python3 scripts/source_check.py --strict --handoff <your-handoff.json>`
   before publishing. `examples/mic-preamp-handoff.json` is a complete example.
7. Hand the handoff to `circuit-design-skill` for simulation and drawings.

## Repository layout

```
SKILL.md                  agent instructions
references/               scope, research, sources, handoff, knowledge documents
catalog/sources.json      source registry
evidence/                 claim records (JSONL)
templates/                requirements, budgets, decision record, measurement, handoff
examples/                 complete handoff example
scripts/source_check.py   registry/evidence/citation/handoff linter
scripts/check_links.py    registry URL checker (opt-in)
tests/                    unit tests
.github/workflows/ci.yml  CI
```

## Status

This repository is built evidence-first. Governance, the registry, the handoff
contract and validator, and four knowledge documents are in place:

- [`references/analog-design.md`](references/analog-design.md) — noise, op-amp
  selection, distortion mechanisms, output stages and a microphone-preamplifier
  case study;
- [`references/power-supplies.md`](references/power-supplies.md) — transformer,
  rectifier and reservoir sizing, LM317/LDO regulators, capacitance
  multipliers, PSRR, fusing and supply layout;
- [`references/grounding-shielding.md`](references/grounding-shielding.md) —
  safety earth, ground loops, balanced interfaces, the pin 1 problem, star
  versus mesh, and the loop breaker;
- [`references/measurement.md`](references/measurement.md) — THD, THD+N, IMD,
  S/N, EIN, CMRR, crosstalk, maximum levels and BS.1770 loudness.

The documents are mostly evidence-backed practitioner guidance, with standards
and peer-reviewed anchors where they exist; each one ends with its sources and
its open gaps. The remaining topics are tracked in
[`references/content-plan.md`](references/content-plan.md), and every
unsupported area is listed in
[`references/source-gaps.md`](references/source-gaps.md).

## Related skills

- [`circuit-design-skill`](https://github.com/davlug3/circuit-design-skill) —
  electrical design, SPICE, KiCad, verification.
- [`pcb-design-skill`](https://github.com/davlug3/pcb-design-skill) — layout,
  DRC/DFM, fabrication outputs.

## License

MIT. Paywalled and restricted sources are linked and cited, never
redistributed.
