# Content Plan

This repository is built evidence-first. A document is written only after its
claims exist in `evidence/` with verified sources. Empty prose is worse than an
honest gap.

## Status

| Area | Document | Status |
|---|---|---|
| Governance | `scope.md`, `research-protocol.md`, `source-policy.md`, `handoff.md` | written |
| Governance | registry, evidence schema, linter, handoff validator, example, CI | written |
| Analog | `analog-design.md` | written, practitioner guidance; gaps recorded |
| Analog | `small-signal-audio.md` | not started; noise, op-amp selection and mic preamp are covered in `analog-design.md` §2, §3 and §6, but the dedicated treatment is still pending |
| Analog | `power-amplifiers.md` | not started; distortion mechanisms and output stages are covered in `analog-design.md` §4 and §5, but thermal/SOA/protection are still gaps |
| Power | `power-supplies.md` | written, practitioner guidance; mains safety details and SMPS are gaps |
| Power | `grounding-shielding.md` | written; includes the ESP/Whitlock leakage reconciliation |
| Topology | `audio-topologies.md` | not started |
| Measurement | `measurement.md` | written; IEC 60268-3/AES17 not yet verified in full text |
| Acoustics | `acoustics.md` | not started |
| Perception | `psychoacoustics.md` | not started |
| Production | `production.md` | not started |

## Research questions per area

### Analog design

- Which device and bias choices set noise, distortion and headroom in an audio
  stage?
- How do feedback, compensation and load interact with stability?
- Which distortion mechanisms dominate in small-signal and large-signal stages?
- How are tolerances and thermal effects budgeted?

### Small-signal audio

- Input protection, RF immunity and common-mode handling.
- Op-amp selection: voltage noise vs current noise vs source impedance.
- Gain blocks, buffers, balanced I/O and impedance bridging.
- EQ and tone-stack topologies and their interaction with source/load.

### Power amplifiers

- Class A/AB/D trade-offs, output-stage topologies, SOA and thermal design.
- Crossover and switching distortion mechanisms.
- Compensation, protection and reactive-load behaviour.

### Power supplies

- Transformer/rectifier/reservoir sizing and ripple.
- Linear regulator, LDO, capacitance multiplier and CRC/CLC trade-offs.
- Switching supplies in audio: noise, layout and PSRR.
- Phantom power, heater supplies, inrush, fusing and safety.

### Grounding and shielding

- Star ground, return currents and ground loops.
- Balanced interconnection and common-mode rejection.
- Shielding, chassis bonding and PCB return paths.

### Measurement

- THD, THD+N, IMD, noise, bandwidth, damping factor and crosstalk.
- Conditions, weighting, bandwidth and fixture effects.
- Bench measurement versus simulation versus listening.

### Acoustics and perception

- Room modes, absorption, diffusion and monitor placement.
- Loudspeaker directivity, impedance and Thiele/Small parameters.
- Masking, equal-loudness contours, audibility and loudness standards.

## Authoring loop

1. Write the question list.
2. Search and register sources.
3. Extract claims to `evidence/<topic>.jsonl`.
4. Write prose from the claims only.
5. Run `scripts/source_check.py --strict`.
6. Search for contradicting sources and record the result.
7. Update `references/source-gaps.md`.
