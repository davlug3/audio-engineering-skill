# Audio Requirements

Fill this before choosing a topology. A number without conditions is not a
requirement.

## 1. Application

| Field | Value |
|---|---|
| Application | |
| Reference product or standard | |
| Signal source | |
| Load | |
| Channels | |
| Environment | |
| Safety class (SELV / mains / phantom / high voltage) | |

## 2. Levels

| Field | Value | Conditions / source |
|---|---|---|
| Nominal input level | | |
| Maximum input level | | |
| Required headroom | | |
| Nominal output level | | |
| Maximum output level | | |
| Gain range | | |

## 3. Bandwidth and impedance

| Field | Value | Conditions / source |
|---|---|---|
| Passband | | |
| Input impedance | | |
| Output impedance | | |
| Load range | | |

## 4. Noise and distortion

| Field | Value | Conditions / source |
|---|---|---|
| Input-referred noise | | bandwidth, source impedance, weighting |
| Output noise | | bandwidth, weighting |
| THD / THD+N | | level, frequency, bandwidth, load |
| IMD method | | test tones and level |
| Crosstalk | | channel pair, level, frequency |

## 5. Power and thermal

| Field | Value | Conditions / source |
|---|---|---|
| Rails | | |
| Current per rail | | |
| Supply rejection target | | |
| Ambient / internal rise | | |
| Cooling | | |

## 6. Acceptance table

| ID | Requirement | Acceptance limit | Test method | Source |
|---|---|---|---|---|
| A1 | | | | |
| A2 | | | | |
| A3 | | | | |

## 7. Assumptions and gaps

List anything the user could not answer, the default chosen, its basis, and the
risk if it is wrong. Record unsupported items in
`references/source-gaps.md`.

## 8. Handoff readiness

- [ ] Every requirement has an acceptance limit and conditions.
- [ ] Every requirement cites a verified source or is marked unverified.
- [ ] Every metric has a measurement method.
- [ ] Safety class has a review plan.
