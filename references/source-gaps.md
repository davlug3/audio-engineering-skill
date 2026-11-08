# Source Gaps

This file records what is **not** yet supported by verified evidence. It is a
feature, not an embarrassment: it prevents confident-sounding prose from
standing in for research.

## Current state

- The registry has 59 entries: 29 `verified` and 30 `candidate`. Only verified
  entries may be cited.
- 190 claim records exist across four evidence files:
  `analog-design.jsonl` (48), `power-supplies.jsonl` (68),
  `grounding-shielding.jsonl` (45) and `measurement.jsonl` (29).
- Four knowledge documents are written: `analog-design.md`,
  `power-supplies.md`, `grounding-shielding.md` and `measurement.md`.
  They are evidence-backed practitioner guidance, not standards claims.
- `python scripts/source_check.py --strict --handoff examples/mic-preamp-handoff.json`
  passes, including the handoff contract checks.

## Gaps by topic

| Topic | What is missing |
|---|---|
| Analog design | Thermal resistance, heatsink sizing and safe operating area for output devices; short-circuit and SOA protection; reactive-load ruggedness; op-amp stability/compensation and capacitive-load isolation; valve design; blind listening evidence for "sound quality" claims |
| Small-signal audio | A dedicated document; input protection beyond the microphone case; RF immunity standards; gain blocks, buffers and impedance bridging; EQ and tone-stack topologies and their source/load interaction |
| Power amplifiers | A dedicated document; thermal/SOA design; protection; reactive-load behaviour; Class-D; valve amplifiers; output-stage distortion beyond Self's measurements |
| Power supplies | Switch-mode supply design for audio; mains creepage, clearance and insulation coordination; UL 6500/UL 62368-1/IEC 60065 full text; transformer thermal design; reservoir capacitor lifetime and ESR derating; bleeder sizing; soft-start component selection; LDO end-of-life stability; PSRR injection fixture |
| Grounding | Shield transfer impedance and shielding-effectiveness numbers; RF immunity standards; UL 943 and IEC 61008/61009 full text; isolation-transformer selection; turntable/tonearm grounding; PCB stackup and return paths; leakage-current measurement method. Premises-wiring magnetic induction is covered by S056, and UL summaries of leakage and GFCI limits by S058/S059, but the standard text and the shield-transfer/PCB-level material are not |
| Measurement | IEC 60268-3 and AES17 in full text; the full text of S057 (only its abstract is used); analyzer calibration; notch-filter design; FFT windowing and leakage; acoustic measurements; psychoacoustic audibility; PSRR fixture; true-peak implementation beyond BS.1770 scope |
| Acoustics | Room modes, absorption, diffusion, monitor placement; loudspeaker directivity and Thiele/Small parameters: no verified sources yet |
| Psychoacoustics | Masking, equal-loudness contours, audibility thresholds and listening-test statistics: no verified sources yet |
| Production | Standards and workflow sources; subjective material must stay labelled |

## Resolved contradictions

### ESP versus Whitlock on leakage current

ESP argues that ground loops are not caused by leakage current because a
leakage path from the active line would trip the safety switch instantly
[C135]. Whitlock documents leakage current from parasitic capacitances as a
real 60 Hz current [C116], with UL limits of 0.75, 3.5 or 5 mA [C115].

The reconciliation is in `grounding-shielding.md` §8: a fault-level leakage
path trips the overcurrent device or a GFCI/RCD [C189][C190], while normal
capacitive leakage is limited to the product-class values in §0, typically
0.5-0.75 mA for cord-and-plug appliances and up to 3.5 mA for some
information-technology equipment with EMI filters [C187]. Whitlock's 3.5/5 mA
summary and ESP's "about 20 mA" RCD figure are practitioner or regional
summaries; neither is a universal standard [C115][C132]. ESP's claim is
recorded with `confidence: low`; it is not used as a design rule.

### Leakage and trip thresholds

The same phrase, "leakage current," covers different measurements and
different limits:

- A UL Class A GFCI trips at 4-6 mA [C189].
- A GFPE for equipment typically trips at 30 mA or higher and is not for
  personnel protection [C190].
- A UL summary of appliance leakage limits gives 0.5 mA for portable
  cord-and-plug appliances, 0.75 mA for fixed or stationary three-wire
  appliances, and up to 3.5 mA for some information-technology equipment with
  EMI filters [C187].
- Whitlock's 3.5/5 mA figures [C115] and ESP's "about 20 mA" RCD figure [C132]
  are different summaries, not interchangeable universal limits.

The exact limit and trip threshold come from the standard and the product
class, not from a single web article.

### Source-policy versus research-protocol

The policy originally required Tier 1 or Tier 2 corroboration for every Tier 3
design rule, while the research protocol required two independent sources.
The policy now says: two independent sources are required; Tier 1/2 is
preferred; where only Tier 3 exists, label the rule **practitioner guidance**
and record the gap. Safety, regulatory and perceptual claims still require the
governing standard or peer-reviewed evidence. This is the rule used by the four
documents above.

## Source access issues

These are known leads that could not be opened in the research session. They
remain `candidate` and are not cited.

- Analog Devices MT-047: the download returned a zero-byte or missing file.
- Jensen Transformers AN003 and AN004: the URLs returned HTML wrappers instead
  of PDFs.
- Some vendor pages block automated downloads or require a browser session.
  Record the failure in the registry note rather than citing from memory.

## Next research priorities

1. Open IEC 60268-3 and AES17 in full text and add clause-level claims for the
   measurement definitions that currently come from RaneNote 145.
2. Add peer-reviewed sources for power-amplifier distortion and thermal/SOA
   design; the current power-amplifier material is mostly Self and ESP.
3. Add a manufacturer application note or standard for output-device SOA and
   heatsink design.
4. Add a source for switch-mode supply noise, layout and PSRR in audio.
5. Add acoustics and psychoacoustics sources before writing those documents.
6. Add a source for shield transfer impedance and RF immunity test levels.
7. Add a source for capacitor lifetime and ESR versus temperature/ripple.
8. Add a blind-listening study before making any "sounds better" claim.
9. Open the full text of S057 and add a clause-level claim for its
   parallel Wiener-Hammerstein measurement procedure.
10. Open UL 6500, UL 943, and IEC 61008/61009 in full text and replace the
    UL and RCD summaries with clause-level claims.

## How to close a gap

1. Add or verify registry entries.
2. Write claim records with locators.
3. Meet the evidence thresholds in `references/research-protocol.md`.
4. Write the document and cite `[C###]`.
5. Remove the gap row and record the date.

## Known risks

- Manufacturer application notes are useful but not independent. Two
  independent Tier 3 sources are acceptable only for implementation rules and
  only when labelled practitioner guidance; safety, regulatory and perceptual
  claims need the governing standard or peer-reviewed evidence.
- Standards are revised. A verified entry can still be `superseded`; check the
  edition before citing.
- Paywalled sources may only support metadata and abstract-level claims unless
  the full text is legitimately available.
- A source can be open and still be wrong. Record the measurement conditions
  and the confidence; do not turn one practitioner's number into a law.
