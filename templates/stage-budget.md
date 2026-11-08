# Stage Budget

One row per stage. Refer all noise to the input so the stages can be compared.

## Conditions

| Field | Value |
|---|---|
| Bandwidth | |
| Source impedance | |
| Load | |
| Temperature | |
| Supply rails | |

## Stages

| Stage | Gain (dB) | Input level | Output level | Headroom | Input Z | Output Z | Noise contribution | Bandwidth | Source |
|---|---|---|---|---|---|---|---|---|---|
| Input protection | | | | | | | | | |
| Stage 1 | | | | | | | | | |
| Stage 2 | | | | | | | | | |
| Output | | | | | | | | | |

## Totals

| Quantity | Value | Limit | Margin | Source |
|---|---|---|---|---|
| Total gain | | | | |
| Input-referred noise | | | | |
| Headroom | | | | |
| Bandwidth | | | | |
| THD budget | | | | |
| Power per rail | | | | |

## Notes

- Show the arithmetic in `scripts/audio_calc.py` or the circuit skill's
  calculators, not in prose.
- A gain distribution is only complete when every stage's clipping point and
  noise contribution are stated.
- Cite `[C###]` for every limit and every device parameter.
