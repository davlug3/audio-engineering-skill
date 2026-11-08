# Scope: Audio Engineering vs Circuit Design

This repository is the audio domain layer. The sibling
[`circuit-design-skill`](https://github.com/davlug3/circuit-design-skill) is the
general electrical engine. Keeping the boundary explicit prevents duplicated,
drifting knowledge.

## Ownership table

| Concern | Owner |
|---|---|
| Requirements, acceptance limits, measurement conditions for audio | audio |
| Audio signal chain, levels, impedance, balancing, gain staging | audio |
| Audio analog topology and part selection | audio |
| Audio power-supply architecture and audio-specific supply practice | audio |
| Transducers, rooms, psychoacoustics, loudness standards | audio |
| Audio measurement and listening-test methodology | audio |
| Generic component sizing, bias calculations, MNA, SPICE netlists | circuit |
| LTspice/KiCad generation, footprints, pin mapping | circuit |
| Vendor SPICE model fetching, provenance, hashing | circuit |
| Generic analog and power formulas (not audio-specific) | circuit |
| PCB layout, DRC/DFM, fabrication outputs | `pcb-design-skill` |

## Resolution rules

1. If the question is **how to make the electrons do X**, it belongs to the
   circuit skill.
2. If the question is **what X must be, why, and how it is judged for audio**,
   it belongs here.
3. If both are needed, this skill writes the requirement and target, and the
   circuit skill implements and verifies. Do not restate the circuit skill's
   formulas; link to them.
4. A generic fact that happens to be used in audio (Ohm's law, a divider) is
   not audio knowledge. Cite the circuit skill or a primary source; do not
   create a competing audio-only version.
5. When ownership is genuinely ambiguous, record the decision in the audio
   repo's `design` notes rather than duplicating the material.

## Worked examples

| Question | Route |
|---|---|
| "What input impedance should a guitar pedal have?" | audio (target and reasons), then circuit (implementation) |
| "Size the bias resistors for this JFET stage" | circuit (calculation and simulation) |
| "Is 0.01% THD audible?" | audio (perception, with sources) |
| "Compute the -3 dB point of this RC network" | circuit (calculator/MNA) |
| "Design a +/-15 V linear supply for a mic preamp" | audio (architecture, ripple/noise targets, grounding), circuit (component sizing and simulation) |
| "Which op-amp for a phono stage?" | audio (noise, input bias, topology, sourced part data), circuit (model fetch and simulation) |
| "Route the board and run DRC" | `pcb-design-skill` |

## What must not happen

- Audio docs copying the circuit skill's generic formulas until they drift.
- The circuit skill embedding audio taste or perceptual claims.
- Either skill claiming measured performance from a simulation.
- Two different answers to the same electrical question in two repos.
