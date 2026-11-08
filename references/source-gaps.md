# Source Gaps

This file records what is **not** yet supported by verified evidence. It is a
feature, not an embarrassment: it prevents confident-sounding prose from
standing in for research.

## Current state

- The registry has verified entries for the source landscape and a set of
  candidates that have not yet been opened.
- No claim records exist yet, so **no audio design document is written**.
- All topics in `references/content-plan.md` are open gaps.

## Gaps by topic

| Topic | What is missing |
|---|---|
| Analog design | Device-level noise/distortion/bias evidence; stability and compensation sources |
| Small-signal audio | Op-amp selection criteria with datasheet evidence; input protection and RF immunity |
| Power amplifiers | Output-stage distortion mechanisms; SOA and thermal design sources |
| Power supplies | Ripple, PSRR, regulator and capacitance-multiplier evidence; SMPS-in-audio practice |
| Grounding | Ground-loop and shielding sources with measurement support |
| Measurement | Standard test conditions and instrument methodology |
| Acoustics | Room, loudspeaker and directivity sources |
| Psychoacoustics | Audibility and masking thresholds from peer-reviewed work |
| Production | Standards and workflow sources; subjective material must stay labelled |

## How to close a gap

1. Add or verify registry entries.
2. Write claim records with locators.
3. Meet the evidence thresholds in `references/research-protocol.md`.
4. Write the document and cite `[C###]`.
5. Remove the gap row and record the date.

## Known risks

- Manufacturer application notes are useful but not independent. Corroborate
  every design rule with a Tier 1 or Tier 2 source.
- Standards are revised. A verified entry can still be `superseded`; check the
  edition before citing.
- Paywalled sources may only support metadata and abstract-level claims unless
  the full text is legitimately available.
