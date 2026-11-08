# Analog Design

This document is the audio-domain companion to the generic electrical engine in
`circuit-design-skill`. It covers the analog signal path from source to power
stage: noise, op-amp selection, distortion mechanisms, output stages and a
microphone-preamplifier case study. It does **not** replace simulation,
schematic capture or design-rule checking.

Every numeric or behavioural statement carries a claim ID. The claim, its
locator and its source are in `evidence/*.jsonl` and
`catalog/sources.json`. Where the evidence is practitioner guidance rather than
a standard or peer-reviewed result, the claim's `confidence` field says so.

## 0. How to use this document

1. Write the design budgets in §1 before choosing a part.
2. Resolve every value against a claim. If no claim exists, write `unverified`
   and add the gap to `references/source-gaps.md`.
3. Send the resulting stage budget and operating points to
   `circuit-design-skill` for simulation and verification; see §7.
4. State the conditions with every result: level, frequency, load, gain,
   bandwidth, weighting and measurement method.

Evidence grade for this document: the noise and distortion material is mostly
Tier 3 practitioner measurement and manufacturer application notes. Tier 1
standards are used for measurement conditions in `measurement.md`, not for the
circuit rules here. The rules below are therefore **evidence-backed
practitioner guidance**, not a standards claim.

## 1. The design budgets

| Budget | What sets it | First estimate | How it is verified |
|---|---|---|---|
| Noise | Source resistance, input device, gain, bandwidth | Source thermal noise plus device voltage/current noise, RMS-summed | Terminated-input EIN measurement at maximum gain |
| Gain and headroom | Source level, maximum output, supply rails | Required gain and peak output plus margin | Sweep level to clipping; compare with supply |
| Bandwidth and slew | Highest full-power frequency, op-amp GBW and slew rate | `SR >= 2*pi*f*Vpeak` | Large-signal sine and square-wave test |
| Distortion | Topology, bias, load, loop gain | Output-stage and input-stage mechanisms | THD/IMD versus level and frequency, plus residual inspection |
| Thermal and SOA | Device dissipation, heatsink, ambient | Not covered here; see gap note | Thermal simulation and measurement |
| PSRR and grounding | Supply rejection, return paths | See `power-supplies.md` and `grounding-shielding.md` | Ripple injection and hum measurement |

A budget is only useful if it is written as a number with conditions. For
example, "noise < 10 uV RMS, 20 Hz-20 kHz, input terminated with 150 Ohm, gain
60 dB" is a budget. "Low noise" is not.

### 1.1 A worked signal-chain budget

Take a line-level chain with a 200 Ohm source, a gain of 100 (40 dB) and a
20 kHz measurement bandwidth. The source thermal noise is 257 nV [C003]. A
5 nV/sqrt(Hz) op-amp contributes 707 nV over the same bandwidth [C009]. The two
are independent, so the input-referred total is

```text
sqrt(707^2 + 257^2) = 752 nV
```

which is -120.3 dBu and a 9.3 dB noise figure relative to the source. The
op-amp, not the source, sets the noise. At the output the noise is 75.2 uV
because the gain is 100. These last three numbers are derived from [C003] and
[C009]; they are not separate source claims.

The lesson is general: below roughly 1 kOhm source impedance, a bipolar op-amp
with a few nV/sqrt(Hz) usually sets the noise; above roughly 10 kOhm, current
noise and the source resistance dominate, and a JFET input becomes attractive
[C006].

## 2. Noise

### 2.1 Thermal noise of a resistor

The thermal noise voltage of a resistor is

```text
V_R = sqrt(4*k*T*B*R)
```

where `k` is Boltzmann's constant, `T` is absolute temperature, `B` is the
noise bandwidth and `R` is the resistance [C001]. The same result is written as
a spectral density `e^2 = 4kTR df`, in `V^2/Hz` [C014]. A spectral density is a
voltage or current per root hertz, in `V/sqrt(Hz)` or `A/sqrt(Hz)` [C015].

Useful anchors at room temperature:

| Resistance | Noise density | Noise over 20 kHz | Level |
|---|---|---|---|
| 100 Ohm | - | 182 nV [C004] | -132.6 dBu (derived) |
| 200 Ohm | - | 257 nV [C003] | -129.6 dBu [C003] |
| 1 kOhm | 4.055 nV/sqrt(Hz), rounded to 4.1 [C002] | 580 nV (derived) | -122.5 dBu (derived) |

The 100 Ohm value is 3 dB below the 200 Ohm value [C004], as expected from the
square root of resistance. Noise rises by 3 dB per doubling of resistance, or
20 dB per factor of 100 [C012]. Temperature matters much less over the
equipment range: a 1 kOhm resistor changes from 4.07 nV/sqrt(Hz) at 29 C to
4.7 nV/sqrt(Hz) at 125 C, a 1.25 dB increase [C013]. Do not spend design effort
on cooling a resistor to reduce its thermal noise; spend it on lowering the
resistance or the bandwidth.

### 2.2 Adding noise sources

Independent noise voltages add in RMS quadrature, not linearly: two equal 1 V
sources sum to 1.414 V, and three 3 mV sources sum to about 5.2 mV [C005]. This
is why a 707 nV op-amp and a 257 nV resistor produce 752 nV, not 964 nV. Always
square, add, then take the square root.

### 2.3 Bandwidth and equivalent noise bandwidth

The integrated noise of a flat spectral density is the density times the square
root of the bandwidth [C009]. For a first-order low-pass response, the
equivalent noise bandwidth is 1.57 times the 3 dB bandwidth [C016]. A
single-pole 20 kHz filter therefore integrates as much noise as a brick-wall
31.4 kHz filter, which is 1.96 dB more noise than the 20 kHz brick-wall value.
Use the actual measurement bandwidth when comparing a calculation with a
measurement; a "20 kHz" number measured through a single-pole filter is not the
same as a 20 kHz flat number.

### 2.4 The op-amp noise model

The standard model places a voltage noise source in series with one input and
a current noise source at each input [C017]. Each source is multiplied by its
gain to the output and the results are RMS-summed [C018]. In a non-inverting
stage the noise gain is `1 + Rf/Rg` [C018]. In an inverting stage at unity
signal gain the noise gain is 2, because the input and feedback resistors
contribute [C007]. For the same source and resistors, an inverting unity-gain
stage therefore has 6 dB more gain for the op-amp's voltage noise than a
non-inverting buffer. This is one reason low-noise designs often use the
non-inverting topology.

Flicker noise has a `1/f` density and is specified by a corner frequency below
which it dominates the white noise [C019]. At low audio frequencies, check the
corner frequency of the candidate part; a part with excellent 1 kHz noise may
be poor at 20 Hz.

### 2.5 Voltage noise versus current noise

Voltage noise dominates at low source impedance; current noise dominates at
high source impedance [C006]. ESP's working split is roughly 1 kOhm to 10 kOhm
for bipolar inputs and 10 kOhm to 100 kOhm for FET inputs [C006]. This is a
design heuristic, not a sharp boundary. The correct test is to compute both
contributions at the actual source impedance and compare them with the source
thermal noise.

A 1 kOhm ideal resistor has 4 nV/sqrt(Hz) of thermal noise, and about 1 kOhm is
a fair estimate of the average output impedance of typical signal sources
[C022]. That makes 4 nV/sqrt(Hz) a useful reference for a "quiet enough"
op-amp in a line-level stage; a 5 nV/sqrt(Hz) part is about 4 dB above the
resistor's own noise, while a 0.9 nV/sqrt(Hz) part is only about 0.2 dB above
it and buys little unless the source is lower impedance or the gain is very
high.

### 2.6 Paralleling devices

Paralleling two identical devices reduces noise by 3 dB, four by 6 dB and eight
by 9 dB; two to six devices is a practical compromise [C010]. The gain is real
but the cost is capacitance, bias current, board area and matching. Paralleling
is most useful in a microphone preamp or a low-output moving-coil stage, where
the source is low impedance and every nanovolt matters.

### 2.7 A measured comparison

ESP measured a 1458 op-amp at about 65 dB signal-to-noise ratio and an LM833 at
about 82 dB, at 46 dB gain with a 200 Ohm source [C011]. The LM833 result is
close to the 83 dB theoretical best for that source. The comparison is a
reminder that the source and the gain set the achievable noise; the op-amp can
only make it worse.

### 2.8 Noise design checklist

1. Record the source resistance and its thermal noise [C001][C003].
2. Record the required bandwidth and whether it is flat or single-pole
   [C016].
3. Select a candidate op-amp and record `en`, `in` and the 1/f corner
   [C019].
4. Compute the noise gain for every source [C018].
5. RMS-sum the source, resistor and device contributions [C005].
6. Compare with the budget and with the source thermal floor.
7. Measure EIN with the input terminated by the expected source impedance at
   maximum gain [C045].
8. If the result is marginal, consider paralleling [C010], a lower-noise
   input device, or a transformer; do not assume a different op-amp will fix a
   source-limited design.

## 3. Op-amp selection

### 3.1 Criteria

ESP's selection criteria are circuit type, required speed, load drive, signal
level, noise, supply voltage, package and cost [C020]. "Sound quality" is not a
selection criterion in the evidence base. If a listening claim is made, treat
it as a hypothesis and design a blind test; see `psychoacoustics.md` when that
document exists.

### 3.2 Typical datasheet values

The following values are ESP's compilation of typical datasheet figures
[C021]. They are useful for an initial shortlist, not for a final design: open
the exact datasheet revision for the part you will buy and check the
conditions.

| Part | Noise (nV/sqrt(Hz)) | Gain-bandwidth (MHz) | Slew rate (V/us) | Input type |
|---|---|---|---|---|
| AD797 | 0.9 | 110 | 20 | Bipolar, low noise |
| LT1115 | 0.9 | 70 | 15 | Bipolar, low noise |
| OPA1612 | 1.1 | 40 | 27 | Bipolar, low noise |
| LM4562 | 2.7 | 55 | 20 | Bipolar |
| NE5532 | 5 | 10 | 9 | Bipolar |
| TL072 | 18 | 3 | 13 | JFET |
| uA741 | 23 | 1 | 0.5 | Bipolar, legacy |

The table is not a ranking. The AD797 and LT1115 are low-voltage-noise parts
for low source impedance; the TL072 is a high-impedance JFET part with poor
voltage noise but low current noise [C024]. The NE5532 is a workhorse for
line-level and 600 Ohm loads [C023]. The LM4562 is a higher-performance
bipolar part [C021].

### 3.3 Source impedance and load

Driving a 600 Ohm load calls for an op-amp rated for the purpose, such as an
NE5532/4, LM4562 or OPA2134; a high-impedance source calls for a JFET-input
op-amp [C023]. The TL072 has higher voltage noise than bipolar audio op-amps
but outperforms them with a high-impedance source [C024]. Do not choose a part
by its noise density alone; check its output current, capacitive-load
capability and stability at the actual load.

### 3.4 Slew rate and full-power bandwidth

The required slew rate for a sine wave is

```text
SR = 2*pi*f*Vpeak
```

A 3 V RMS, 20 kHz sine has a peak of 4.24 V and requires 0.53 V/us. A 741 with
0.5 V/us is therefore at its limit at that condition; ESP's statement that a
741 can provide about 3 V RMS at 20 kHz is an approximation, and the exact
part, supply and load must be checked [C025]. At 10 V RMS and 20 kHz the
requirement is 1.78 V/us. Calculate the number for the highest full-power
frequency you specify, not for 1 kHz.

### 3.5 Distortion

Douglas Self measured NE5532/4 distortion below 0.0005% at all frequencies
below 10 kHz with a 5 V RMS output on +/-18 V supplies [C026]. That is a
useful sanity check on the "op-amps are the bottleneck" assumption: in a
well-designed line stage, the op-amp may be far more linear than the output
stage or the measurement system.

### 3.6 Stability, decoupling and protection

These are not yet backed by a numeric claim in this registry. Treat them as
verification tasks, not as rules:

- Check the datasheet's capacitive-load limit and recommended isolation.
- Check decoupling and supply bypass requirements for the exact package.
- Check input bias current, input offset and output swing at the actual
  supply.
- Simulate the loop gain and phase margin in `circuit-design-skill`.
- Verify with a square-wave and a reactive-load test.

Record any value you use in `evidence/*.jsonl` before putting it in
a design.

## 4. Distortion

### 4.1 Eight mechanisms

Self organizes a generic Class-B power amplifier around eight distortion
mechanisms: input stage, VAS, output stage (large-signal nonlinearity,
crossover and switchoff), VAS loading, decoupling return and rail induction,
feedback takeoff point, and capacitor nonlinearity [C027]. The list is a design
checklist, not a claim that every amplifier has all eight at equal strength.

| Mechanism | Physical cause | Typical symptom | Design response |
|---|---|---|---|
| Input stage | Transconductance varies with signal; imbalance | Rising HF distortion; 12 or 18 dB/octave slope | Balance the pair; degeneration; more loop gain [C036][C037][C047] |
| VAS | Nonlinear Early effect and loading | Broadband distortion that rises with output level | Cascode, buffer or local feedback [C035] |
| Output LSN | Gain falls as current rises; beta droop | Third harmonic, worse below 8 Ohm | More output devices; sustained-beta devices [C031][C032] |
| Crossover | Dead zone around the bias point | High-order spikes at all levels | Correct bias; CFP or error correction [C028][C033] |
| Switchoff | Charge storage reverse-biases the base-emitter junction | HF distortion that rises with frequency | Speed-up capacitor; Baker clamp; CFP [C034] |
| VAS loading | Nonlinear input impedance of the output stage | Distortion that tracks output-stage current | VAS buffer or local feedback [C035] |
| Decoupling and rails | Shared supply impedance and rail induction | Distortion that changes with layout and decoupling | Separate returns; decouple at the stage [C027] |
| Feedback takeoff | Feedback taken from the wrong point | Distortion that cannot be reduced by more loop gain | Take feedback from the output line, not from a point inside the output-stage wiring [C027] |
| Capacitor nonlinearity | Dielectric absorption and voltage coefficient | Low-frequency distortion that rises at 6 dB/octave | Use a linear dielectric; avoid signal-path electrolytics [C048] |

### 4.2 Input stage

The input pair's transconductance is greatest at zero differential input and is
proportional to tail current; emitter degeneration linearizes the pair but
reduces the available negative feedback factor [C036]. Input-stage distortion
rises at 12 dB/octave when the stage is unbalanced and 18 dB/octave when
balanced, because the signal current needed to drive the dominant compensation
capacitor doubles each octave while loop gain falls 6 dB/octave [C037]. A 2%
collector-current imbalance raised THD from 0.10% to 0.16% at -45 dBu, and a
10% imbalance raised it to 0.55%; balance should be within 1% for lowest
high-frequency distortion [C047]. Matching matters.

### 4.3 Output stage

At +/-40 V, Self's CFP output stage produced 0.014% THD at 8 Ohm and 0.030% at
4 Ohm, versus 0.031% and 0.042% for the emitter-follower stage [C029]. In the
same comparison a simple MOSFET output stage produced 0.47% at 8 Ohm and 0.84%
at 4 Ohm [C030]. These are specific measurements at specific conditions; do not
generalize them to every CFP, EF or MOSFET design. They do show that topology
and bias details can change distortion by more than an order of magnitude.

Large-signal nonlinearity increases as load impedance falls below 8 Ohm, and
the third harmonic appears and dominates at low loads [C031]. Output-device beta
droop causes gain droop; paralleling two output devices reduces distortion by
about 1.9 times, and sustained-beta devices reduce 4 Ohm distortion by about 1.4
times [C032].

### 4.4 Crossover and bias

Crossover distortion occurs over a small part of the transfer characteristic,
generates high-order harmonics, and is present at all output levels; the THD
percentage can rise as output level falls [C028]. This is why a THD sweep that
only reports a number at full power can miss the problem. Optimal Class-B bias
is set by the voltage between the output-device emitters, not by quiescent
current alone; changing emitter resistors from 0.1 Ohm to 0.47 Ohm changes the
optimal quiescent current but barely changes the required bias voltage [C033].
Bias by voltage and verify by distortion residual, not by a quiescent-current
number copied from another design.

### 4.5 Switchoff and VAS loading

An emitter-follower output stage can reverse-bias an output device's
base-emitter junction during switchoff by about -0.5 V at 8 Ohm and -1.6 V at
4 Ohm; a 1 uF speed-up capacitor can halve THD at 40 kHz [C034]. VAS loading
distortion is caused by the nonlinear input impedance of the Class-B output
stage; a VAS buffer or local feedback linearizes it [C035].

### 4.6 The "Blameless" result

Self's "Blameless" Class-B design achieves below 0.0005% THD at 1 kHz and
0.003% at 10 kHz [C038]. Treat it as an existence proof: a carefully biased
Class-B amplifier can be very linear without Class-A operation. It is not a
guarantee for a different topology, layout or parts.

## 5. Power-amplifier design procedure

1. **Define the load and power.** State continuous and peak power, load
   impedance, reactive-load angle and duration.
2. **Choose the output stage.** Compare EF, CFP and MOSFET at the actual load
   and supply [C029][C030]. Do not choose by reputation.
3. **Set the bias.** Use the emitter-to-emitter voltage method [C033] and
   verify with a distortion residual.
4. **Check large-signal behaviour.** Include the lowest specified load [C031]
   and the beta-droop behaviour of the chosen devices [C032].
5. **Check switchoff and VAS loading.** Add a speed-up capacitor or clamp if
   needed [C034]; buffer the VAS if the output stage loads it [C035].
6. **Size the supply.** See `power-supplies.md`; the reservoir, rectifier,
   fuse and transformer rules are there.
7. **Design the grounding and shielding.** See `grounding-shielding.md`.
8. **Verify.** Sweep THD and IMD versus level and frequency; inspect the
   residual for crossover spikes; measure noise with a terminated input;
   measure output impedance and damping; run a thermal soak at the worst-case
   signal.

Thermal design, safe operating area, short-circuit protection and reactive-load
ruggedness are **not yet evidenced** in this registry. Do not invent numbers
for them. Use the device datasheet's SOA curves, the supplier's thermal
application notes and a thermal simulation, and record the sources before
publishing a rule.

## 6. Microphone-preamplifier case study

### 6.1 Requirements

A microphone preamplifier must provide low noise with low source impedance,
high signal handling, RF immunity, high common-mode rejection, variable
differential gain from 1 to 1000 or more, and usually +48 V phantom power
[C039]. These requirements conflict: phantom protection adds series resistance
and capacitance, the pad changes the source impedance, and high gain amplifies
every input error.

### 6.2 Noise

A 150 Ohm source at room temperature has a thermal-noise limit of -131 dBu over
20 kHz and -134 dBu over 10 kHz [C046]. A 5 nV/sqrt(Hz) op-amp over 20 kHz is
707 nV [C009], which is -120.8 dBu, about 10 dB worse than the source. Even
after RMS-summing with the 218 nV source noise, the total is about 740 nV and
the noise figure is about 10.6 dB (derived from [C009] and [C046]). To be within
1 dB of the source limit, the input device's voltage noise must be below about
0.78 nV/sqrt(Hz) over 20 kHz (derived). This is why microphone preamps use
low-noise bipolar input devices, paralleled devices or transformers, and why a
generic 5 nV/sqrt(Hz) op-amp is not a microphone preamp.

Measure EIN at maximum gain with the input terminated by the expected source
impedance; the standard source impedance is 150 Ohm [C045]. Report the
bandwidth and weighting with the number.

### 6.3 Phantom power and protection

Phantom-power faults can apply -48 V to a preamplifier input; protection
requires series resistors, diode clamps and capacitors that absorb charge
[C040]. Phantom feed resistors should be thin film, matched to 1% or better, and
rated for the shorted-input dissipation of 0.338 W each [C043]. Do not use
carbon film or low-power resistors here; the fault condition is a normal
operating condition for a microphone input.

### 6.4 Pad and input impedance

A 20 dB balanced U-pad can keep the input impedance near 2 kOhm and reduce
resistor matching errors; a bipolar-input preamplifier should see a differential
source impedance no higher than about 2 kOhm [C041]. The pad also attenuates
the signal before the input stage, which protects the stage from line-level
signals and phantom transients.

### 6.5 RF immunity

RF immunity is improved by capacitors at the input connector returned to the
connector shield, plus a third capacitor to shunt differential RF inside the
enclosure [C042]. The shield return must go to the chassis at the connector, not
to the signal ground; see `grounding-shielding.md`.

### 6.6 Headroom

With +/-15 V supplies the THAT 1570 accepts at least +26.8 dBu differential
input at unity gain without clipping [C044]. Check the maximum input at the
gain you will use, not only at unity; a pad may be needed for line-level
signals.

### 6.7 Layout checklist

- Input connector shell and shield to chassis at the entry point
  [C109][C110].
- RF capacitors at the connector, returned to the shield [C042].
- Phantom resistors matched and rated [C043].
- Keep the input pair and its bias network away from the supply and output
  wiring; see `grounding-shielding.md`.
- Star the audio return at the input stage and keep the return current out of
  the shield [C124][C125].

## 7. Handoff to `circuit-design-skill`

The audio skill owns the targets, conditions and interpretation. The circuit
skill owns the netlist, simulator, schematic and verification. The handoff is
the JSON contract in `references/handoff.md`.

Send:

- the stage budget: gain, input and output levels, source and load impedance,
  bandwidth, noise target, distortion target and supply;
- the topology and the operating points you intend;
- the part numbers and the datasheet revisions;
- the test conditions that define pass/fail.

Ask for:

- DC operating point and device dissipation;
- AC gain, phase margin and bandwidth;
- input-referred noise over the specified bandwidth;
- THD/IMD versus level and frequency, with the residual available;
- transient response and slew limiting;
- PSRR and supply-ripple transfer;
- a verification report that states the simulator, models and conditions.

The circuit skill's `metrics` stage is not implemented yet; until it is, export
the raw simulation data and compute the metrics with the definitions in
`measurement.md`. Do not accept a single THD number without the conditions
[C166].

## Sources

All sources below were opened on 2026-11-08. Claim locators are in
`evidence/*.jsonl`.

- [S040] Rane Technical Staff, *RaneNote 110: Sound System Interconnection*,
  written 1985, revised 11/15.
  <https://www.ranecommercial.com/legacy/note110.html>
- [S041] Dennis Bohn, *RaneNote 145: Audio Specifications*, Rane Corporation,
  written 2000, revised 1/03.
  <https://www.ranecommercial.com/legacy/note145.html>
- [S045] Rod Elliott, *Noise in Audio Amplifiers*, Elliott Sound Products,
  copyright 1999, updated May 2025. <https://sound-au.com/noise.htm>
- [S047] Rod Elliott, *Opamp Selection*, Elliott Sound Products, September
  2025. <https://sound-au.com/articles/opamp-selection.htm>
- [S049] Texas Instruments, *Noise Analysis in Operational Amplifier Circuits*,
  application report SLVA043B, 2007. <https://www.ti.com/lit/pdf/slva043>
- [S054] THAT Corporation, *Input and Output Circuits for THAT Preamplifier
  ICs*, Design Note 140, Doc 600140 Rev 03, 2011-2014.
  <https://thatcorp.com/datashts/dn140.pdf>
- [S055] Douglas Self, *Distortion In Power Amplifiers*, updated 12 September
  2019. <http://www.douglas-self.com/ampins/dipa/dipa.htm>

## Unverified and open gaps

- Thermal resistance, heatsink sizing and safe operating area for output
  devices: no verified source in the registry yet.
- Short-circuit protection, SOA protection and reactive-load ruggedness: no
  verified source yet.
- Op-amp stability, capacitive-load isolation and decoupling: no numeric claim
  yet; simulate and use the exact datasheet.
- Valve (tube) design: no verified source yet.
- "Sound quality" differences between op-amps: no blind-test evidence in the
  registry; treat as a hypothesis.
- Exact datasheet revisions for the op-amps in the table: ESP's compilation is
  a secondary source; verify each part before production.

See `references/source-gaps.md` for the live list.
