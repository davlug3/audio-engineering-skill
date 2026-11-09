# Audio Engineering Skill — Roadmap and Work Plan

Status: agreed scope; implementation ongoing.
Date: 2026-11-09.

This is the working plan and status record for the two sibling repositories. It
is not a knowledge document and does not carry design claims. The public
evidence is in `catalog/` and `evidence/`; the live coverage gaps are in
`references/source-gaps.md`.
Repos:

- `circuit-design-skill` — general electrical engine (unchanged owner of SPICE, KiCad, MNA, models, verification).
- `audio-engineering-skill` — new sibling; audio/music/sound-engineering domain, audio analog design and audio power-supply design.

## 1. Goal

Give the agent defensible audio-engineering knowledge and a repeatable method:

1. define the audio signal chain, levels and budgets;
2. choose a topology and parts from sourced evidence;
3. hand the electrical implementation to `circuit-design-skill` for simulation, drawings and verification;
4. state what is evidenced, what is simulated and what is still unverified.

## 2. Scope and boundary

| Topic | Canonical home |
|---|---|
| Component sizing, MNA, ngspice, KiCad, SPICE models, generic analog/power formulas | `circuit-design-skill` |
| Audio signal chain, levels, impedance, gain staging | `audio-engineering-skill` |
| Audio analog design: preamps, line/phono stages, headphone and power amplifiers, pedals, crossovers | `audio-engineering-skill` |
| Audio power supplies: linear/LDO, capacitance multipliers, CRC/CLC, SMPS, PSRR, phantom/heaters, grounding | `audio-engineering-skill` |
| Transducers, room acoustics, psychoacoustics, loudness standards | `audio-engineering-skill` |
| Audio measurement and listening-test methodology | `audio-engineering-skill` |
| Music/sound-engineering workflow and standards | `audio-engineering-skill` (bounded, labelled subjective where applicable) |
| Simulation execution and numeric metric extraction | `circuit-design-skill` (generic `metrics` stage, future) |

Rule: *how to make the electrons do X* → circuit skill. *What X must be, why, and how to judge it for audio* → audio skill.

No runtime import between repos. The only coupling is a versioned JSON handoff.

## 3. Research-first policy (non-negotiable)

- Never answer an audio-circuitry question from memory. Recall may produce hypotheses and search queries only.
- Every value, limit, formula, topology, part, pinout, standard or failure mode must be traced to a source opened in the current session.
- Open the source; do not trust snippets or summaries. Record the locator (section/page/clause/figure).
- Minimum evidence: one primary source per part parameter; two independent
  sources per design rule or limit; three where sources conflict. Where only
  Tier 3 evidence exists, label the rule **practitioner guidance** and record
  the gap; safety, regulatory and perceptual claims still require the governing
  standard or peer-reviewed evidence.
- Conflicts are recorded, not averaged.
- Check for superseded datasheets and standard editions.
- If the web is unavailable, say so and produce a research plan; never fill the gap from memory.
- Answers carry a **Sources** section listing only what was opened, and label unverified material as hypothesis.

## 4. Source registry and evidence model

```
catalog/sources.json      registry of sources
evidence/<topic>.jsonl    one claim per line, linked to a source id and locator
references/*.md           prose that cites [C###] / [S###]
references/source-gaps.md explicit unsupported areas
```

Source tiers:

1. Standards bodies and peer review: ITU, IEC, ISO, AES standards; JAES, JASA/JASA-EL, IEEE, Applied Acoustics, JSV.
2. Books and monographs with ISBN and edition.
3. Practitioner engineering: manufacturer datasheets/app notes, named-author technical articles.
Excluded as citations: forums, wikis, anonymous or undated pages, marketing without data, LLM output.

Registry entry fields: `id`, `tier`, `title`, `authors`, `year`, `venue`, `doi`, `url`, `accessed`, `status` (`verified|candidate|broken|superseded`), `access` (`open|paywalled|book`), `topics`, `note`.

Only `verified` sources may be cited. Paywalled work is linked and cited, never mirrored.

Coverage target: at least three independent sources per major topic, at least one Tier 1. Missing coverage is recorded in `source-gaps.md`.

Maintenance: quarterly link/DOI checks (opt-in CI), superseded-standard tracking, Wayback snapshot for fragile pages.

## 5. Curricula

Written references (each authored from evidence, with a `## Sources` section):

- `analog-design.md` — devices, bias, small-signal, feedback, stability, noise,
  distortion mechanisms, tolerances, and the microphone-preamplifier case
  study. Thermal/SOA material now lives in `power-amplifiers.md`.
- `small-signal-audio.md` — levels, impedance, gain blocks, buffers, balanced
  and unbalanced I/O, input protection, RF immunity and tone controls.
- `power-amplifiers.md` — load envelope, output stages, thermal chain, SOA and
  derating, short-circuit and speaker protection, reactive loads and Class-D
  thermal notes. Tier 3 practitioner guidance; gaps recorded.
- `power-supplies.md` — transformer/rectifier/reservoir, ripple, linear/LDO,
  capacitance multipliers, CRC/CLC, PSRR, decoupling, inrush, fusing and
  supply layout.
- `grounding-shielding.md` — safety earth, star ground, ground loops, balanced
  interconnection, shielding and return paths.
- `measurement.md` — THD/IMD/noise/response/damping factor, conditions, bench
  versus simulation, and BS.1770 loudness.

Planned references (not yet written):

- `audio-topologies.md` — mic pre, RIAA phono, line, headphone, pedal,
  crossover and power-amplifier architectures.
- `acoustics.md` — rooms, modes, absorption, monitors, SPL and directivity.
- `psychoacoustics.md` — masking, audibility, loudness and perception limits.
- `production.md` — bounded workflow/standards material, labelled subjective
  where it is taste.

Governance documents: `research-protocol.md`, `source-policy.md`, `scope.md`,
`handoff.md` — written.

Templates: requirements, stage budget, PSU budget, measurement plan, listening
test and handoff JSON — written.

Scripts: `source_check.py` (registry/evidence/citation/handoff linter) and
`check_links.py` (opt-in URL check). The circuit skill's `audio_handoff.py`
performs the merge. Sourced calculators are a future item; any calculator must
return the source id for every formula and constant.

## 6. Handoff contract v1

The audio skill emits:

```json
{
  "handoff_version": 1,
  "application": "electric-guitar pedal",
  "conditions": {"input_vrms": 0.1, "frequency_hz": 1000, "load_ohm": 10000},
  "requirements": [{"id": "A1", "text": "...", "acceptance": "...", "source": "S012"}],
  "metrics": [{"measure": "gain_db", "target": 0.0, "tolerance": 0.5, "requirement": "A1"}],
  "sources": [{"id": "S012", "title": "...", "url": "..."}]
}
```

The circuit skill merges `requirements` into `design.requirements` and `metrics` into its generic `metrics` block, then validates that every `requirement` reference exists. Handoff remains valid without either repo installed.

## 7. Circuit-skill changes

1. **Done:** `references/audio-handoff.md` exists, with cross-links in
   `SKILL.md`, `README.md` and `references/intake.md`.
2. **Done:** the planned `audio` verification block is now the generic
   `metrics` stage at `82ac355`. Extraction (gain, bandwidth, THD, noise,
   transient RMS) stays in the circuit skill; the audio skill supplies targets
   and interpretation.
3. **Done:** optional sibling discovery (`AUDIO_ENGINEERING_SKILL`
   environment variable, `--audio-skill` and relative search) validates a
   handoff's cited sources against the audio registry; `--require-registry`
   makes a missing sibling fatal.
4. **Rule:** do not duplicate audio knowledge in the circuit skill. The audio
   skill owns the targets, conditions and interpretation; the circuit skill
   owns the netlist, simulator, schematic and verification.

## 8. CI

Audio repo:

- 26 unit tests for `source_check.py`;
- registry/evidence/citation validation;
- handoff validation with `--handoff examples/mic-preamp-handoff.json`;
- opt-in external link/DOI reachability job.

Circuit repo:

- existing suite must stay green (206 tests, 2 skipped locally);
- ngspice metrics example `examples/rc-lowpass-metrics.json` with
  `--require simulate`;
- cross-repo job that checks out both repos, runs the audio linter on
  `examples/mic-preamp-handoff.json`, merges it with
  `examples/mic-preamp-base.json` and `examples/mic-preamp-map.json`, and
  validates the merged spec.

## 9. Sequencing

1. **Done:** scaffold repo, license, scope, research protocol, source policy,
   handoff contract, registry seed, linter, tests and CI.
2. **Done:** cross-link the circuit skill.
3. **Done:** source sweep and coverage matrix; gaps are published in
   `references/source-gaps.md`.
4. **Done:** analog and PSU references authored from evidence; small-signal and
   power-amplifier references added later.
5. **Partly done:** `measurement.md` is written. Acoustics, psychoacoustics and
   production remain.
6. **Done:** generic `metrics` stage and handoff merge implemented in the
   circuit skill.
7. **Done:** integration example and CI gate.

## 10. Acceptance criteria

- Every reference doc has a `## Sources` section and resolvable citations.
- `source_check.py` passes in CI with no unregistered citations.
- No numeric claim or part recommendation without an evidence record.
- Handoff example validates against the contract and merges into a circuit spec.
- Circuit skill stays green; the metrics stage is additive and every existing
  spec remains valid.
- Known gaps are listed, not hidden.

## 11. Non-goals

- Not an autonomous audio product designer.
- Not a substitute for bench measurement or listening tests.
- No claim that a simulation "sounds like" a reference device.
- No mirrored paywalled papers or restricted vendor models.
- No creative-production advice presented as engineering fact.

## 12. Work state (2026-11-09)

### Audio repo (`davlug3/audio-engineering-skill`)

- `main` at `295b1ee`; CI run `42541016179` passed on the power-amplifier
  document, including the handoff example.
- Registry: 66 sources, 36 `verified`, 30 `candidate`.
- Evidence: 267 claims across `analog-design.jsonl` (48),
  `small-signal.jsonl` (31), `power-amplifiers.jsonl` (46),
  `power-supplies.jsonl` (68), `grounding-shielding.jsonl` (45) and
  `measurement.jsonl` (29).
- Written knowledge documents: `analog-design.md`, `small-signal-audio.md`,
  `power-amplifiers.md`, `power-supplies.md`, `grounding-shielding.md`,
  `measurement.md`. Each has a `## Sources` section and a gaps note.
- Tier 1 anchors: ITU-R BS.1770-5; AES Convention Paper 8234 (Whitlock and
  Fox, 2010); JAES 74(5) (Parolo, 2026, abstract-level); UL leakage and GFCI
  summaries S058/S059.
- Governance: `source_check.py` validates the registry, evidence, citations and
  handoff JSON (`--handoff`), with 26 unit tests. `examples/mic-preamp-handoff.json`
  is a complete, CI-validated handoff.
- Planned but not written: `audio-topologies.md`, `acoustics.md`,
  `psychoacoustics.md`, `production.md`.

### Circuit repo (`davlug3/circuit-design-skill`)

- `main` at `82ac355`; the metrics work is committed and pushed. CI run
  `42494227611` passed on that commit.
- Generic `metrics` stage implemented:
  - `scripts/ngspice_raw.py` parses real ASCII rawfiles, including complex
    frequency columns, blank lines between points, multi-variable rows and
    informational lines in the variable table.
  - `scripts/metrics.py` extracts `gain_db`, upper/lower/width bandwidth,
    `.four` THD, input/output noise and transient RMS, and compares targets or
    limits.
  - `scripts/verify.py` adds a `metrics` layer after ngspice; a missing
    ngspice is a skip, but a declared metric that cannot be evaluated is a
    failure.
  - `scripts/design_spec.py` validates the `metrics` block, analysis links,
    requirement links, and normalized output names.
  - `scripts/generate.py` emits `.four` for a `fourier` analysis.
  - `scripts/audio_handoff.py` merges the audio handoff, a base circuit spec
    and a test-point map, then validates the merged spec.
- `references/metrics.md` documents definitions, analysis requirements,
  accrued errors and limits; `references/audio-handoff.md` documents the merge.
- `examples/rc-lowpass-metrics.json` is verified by CI with ngspice and
  `--require simulate`; `examples/mic-preamp-base.json` and
  `examples/mic-preamp-map.json` back the cross-repo merge job.
- CI has a cross-repo job that checks out both repos, runs the audio linter on
  `examples/mic-preamp-handoff.json`, merges it, and validates the result.
- CI run `42494227611` passed on `82ac355`: unit tests, the cross-repo merge,
  and the ngspice metric example. The metric evidence was
  `M1: gain_db=-1.44507 dB (PASS; target -1.4451 +/- 0.01)` and
  `M2: bandwidth_hz=1587.82 Hz (PASS; target 1591.55 +/- 31.83)`.
- Audio run `42494227297` passed on `fd738ac`; run `42497434683` passed on
  `2b9df0c` with the small-signal document and 31 new claims; run
  `42541016179` passed on `295b1ee` with the power-amplifier document and 46
  new claims.
- Test suite: 206 tests pass (2 skipped) locally; ngspice, KiCad and the live
  model fetch run on CI.

### Next actions

1. Open the standard texts in `source-gaps.md`: IEC 60268-3, AES17, UL 6500,
   UL 943, IEC 61008/61009; add clause-level claims and replace summaries.
2. Add acoustics and psychoacoustics sources before writing those documents.
3. Add ESD/line-overvoltage, RF-immunity test-level, parametric-EQ and
   transformer-selection sources for the small-signal document.
4. Add a Tier 1/2 thermal/SOA source and a second independent source for
   loudspeaker-protection relay DC practice; then remove those gaps from
   `power-amplifiers.md`.
5. Extend the metrics stage only where audio needs it (IMD, PSRR versus
   frequency, weighted noise, FFT distortion); keep the generic extraction in
   the circuit skill and the interpretation in the audio skill.
