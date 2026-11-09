# Power Amplifiers

This document covers the power stage: the load it must drive, output-stage
choice, thermal design, safe operating area (SOA), protection and reactive-load
ruggedness. It is a companion to `analog-design.md` §4-§5, which covers the
distortion mechanisms and the basic design procedure, and to
`power-supplies.md`, which covers the rails that feed the stage.

It is not a construction manual and it is not a substitute for a device
datasheet, a thermal simulation or bench testing. The thermal and SOA material
here is **Tier 3 practitioner guidance**. It is corroborated by several
independent vendor and practitioner sources, but no Tier 1 or Tier 2 source for
power-amplifier thermal design is registered yet. That gap is recorded at the
end of this document and in `references/source-gaps.md`.

Every numeric or behavioural statement carries a claim ID. The claim, locator
and source are in `evidence/*.jsonl` and `catalog/sources.json`.

## 0. How to use this document

Write the power-stage requirement before choosing a topology or a transistor:

- continuous and peak output power, with the test conditions;
- load impedance magnitude **and phase** versus frequency;
- the lowest impedance the amplifier must survive, not just the nominal value;
- supply voltage at low line, nominal and high line;
- ambient temperature at the hottest point around the equipment;
- duty cycle, crest factor and expected programme material;
- fault cases: shorted output, short to either rail, fan failure, DC offset;
- the protection behaviour that is acceptable when a fault occurs.

The output of this stage is a design intent: topology, device type, number of
output pairs, thermal path, protection scheme and the conditions that the
circuit skill must verify. The audio skill owns the targets and the
interpretation; the circuit skill owns the netlist, simulation and
verification.

## 1. The load defines the amplifier

### 1.1 Power is not a single number

An amplifier is not specified by one wattage. The same output power can mean a
different voltage, current, dissipation and SOA stress depending on the load
and the signal. State continuous power, peak power, load, supply, frequency,
bandwidth and distortion together. A THD or THD+N number without test
frequency, level, gain, load and bandwidth is not a specification [C166].

Nominal impedance is a label, not a constant. A nominal 8 Ohm loudspeaker may
fall to 3 Ohm or less and rise to 50 Ohm or more at driver resonance, and a
nominal 4 Ohm loudspeaker may have a minimum near 3 Ohm [C234]. Design for the
minimum impedance and the phase angle, not the label.

Music is also not a sine wave. Crest factor can be as low as 6 dB and as high
as 20 dB, a 100:1 power ratio; a 10 dB crest factor is a common assumption
[C259]. The average dissipation that sizes the heatsink and the instantaneous
dissipation that tests the SOA are therefore different calculations
[C223][C230].

### 1.2 The load is reactive

At a 45 degree load phase angle, peak transistor dissipation doubles and the
power delivered to the load is halved; this is the worst case [C235]. In ESP's
worked example, a 3 Ohm load with 45 degree phase at +/-35 V produces almost
200 W peak transistor dissipation and about 43 W average, with the peak at the
voltage zero crossing [C236]. That is not a small margin problem: the average
may look comfortable while the peak is at the device rating.

A purely reactive load delivers no real power, so the amplifier dissipates all
the power drawn from the supply; at full output this is about three times the
worst-case dissipation with a resistive load [C226]. Real loudspeakers are not
purely reactive, but the trend is the same: the further the phase is from zero,
the less of the supply power reaches the load and the more heats the output
devices [C234][C235].

Speaker-cable resistance can mitigate the inductive part of a difficult load,
but it wastes power and changes the load the amplifier sees [C265]. Do not use
cable resistance as a design fix.

### 1.3 Supply voltage and stress

Higher rails increase the voltage across the conducting output device and the
peak dissipation for the same load current [C236]. The supply at high line is
therefore part of the SOA check, not just the power calculation. Transformer
secondary voltage is specified at full rated current, so the unloaded DC rail
can be higher than the nominal calculation [C170]. Use the high-line rail for
the SOA and short-circuit checks.

## 2. Output stage: distortion is only one axis

`analog-design.md` §4 covers the distortion mechanisms in detail. This section
adds the constraints that decide whether a low-distortion stage can survive.

Self's measurements at +/-40 V show the spread that topology and bias can
produce: the CFP stage gave 0.014% THD at 8 Ohm and 0.030% at 4 Ohm, the
emitter-follower gave 0.031% and 0.042%, and a simple MOSFET stage gave 0.47%
and 0.84% [C029][C030]. These are specific measurements at specific
conditions, not a ranking for every implementation.

| Output stage | Distortion evidence | Thermal and drive consequences |
|---|---|---|
| Emitter follower (EF) | 0.031% at 8 Ohm, 0.042% at 4 Ohm in Self's comparison [C029] | Robust drive, but switchoff can reverse-bias the base-emitter junction [C034] |
| Complementary feedback pair (CFP) | 0.014% at 8 Ohm, 0.030% at 4 Ohm in the same comparison [C029] | Lower distortion, but local stability and bias detail need care |
| Lateral MOSFET | No comparable number in this registry | No second breakdown; limited mainly by average power, but self-limiting is not protection [C239] |
| Switching (vertical) MOSFET | No comparable number in this registry | Not recommended for linear use; thermal runaway and poor gain linearity are concerns [C239] |
| Class-D | Not a linear output stage; not comparable to the numbers above | Higher efficiency, but loss is not negligible and still needs a thermal path [C245] |

The lowest-THD stage is not automatically the right choice. A device that is
run close to its SOA, or a stage whose protection misbehaves on a reactive
load, can fail even when its small-signal distortion is excellent [C223][C229].
Check distortion and ruggedness together.

## 3. Thermal design

### 3.1 The thermal chain

Heat flows from the device junction to the case, through the interface
material, into the heatsink and then to the ambient air. For a top-mounted
heatsink the simplified model is [C243][C249]:

```
theta-JA = theta-JC + theta-CH + theta-HA
PD       = (TJ - TA) / theta-JA
```

Where:

- `theta-JC` is the junction-to-case thermal resistance, fixed by the device
  package and die;
- `theta-CH` is the case-to-heatsink resistance, set by the interface material,
  flatness, mounting pressure and insulation;
- `theta-HA` is the heatsink-to-ambient resistance, set by the heatsink, its
  orientation and the airflow;
- `TJ` is the junction temperature, `TA` the ambient temperature and `PD` the
  dissipated power.

Increasing heatsink surface area reduces thermal resistance; the simplified
relationship is `theta-JA = 1/(hc A)`, so the resistance also falls when
natural convection is replaced by forced convection [C248]. The interface and
heatsink terms must both be minimized [C249]. An electrically isolating Kapton
washer adds roughly twice the thermal resistance of a direct or grease-coupled
joint [C261].

A heatsink's datasheet resistance varies with power level, orientation and
airflow, so read the rating for the actual mounting and flow conditions
[C250]. In natural convection, place heat sources near the top of the
enclosure, avoid temperature-sensitive circuits above them, and orient
heatsinks so air can pass freely over all fins [C251]. These layout points are
**practitioner guidance** from one source; verify them in the actual enclosure.

Ambient is not room temperature. For electronics it is the temperature of the
air surrounding the equipment at its hottest point; an enclosed cabinet can
reach 50 C when the room is 25 C [C260]. Measure the real ambient, including
the effect of other equipment and restricted ventilation.

Reliability falls as junction temperature rises; Apex's normalized failure-rate
curve, based on MIL-HDBK-217F, increases with temperature [C252]. A design that
merely survives the thermal calculation is not the same as a design with a
useful life.

#### Two worked thermal examples

These are two different examples, not a comparison of technologies.

| Quantity | TI Class-D example [C244] | ESP Class-AB example [C233] |
|---|---|---|
| Dissipation | 13.6 W for 80 W into 4 Ohm | 20 W continuous per transistor |
| Junction-to-case | 0.6 C/W | 0.54 C/W |
| Case-to-heatsink | included in the 3.44 C/W case-to-ambient budget | 1 C/W |
| Heatsink-to-ambient | included in the 3.44 C/W budget | 4 C/W |
| Ambient | 75 C | 25 C |
| Junction temperature | 130 C design limit | about 135 C resulting |
| Result | case-to-ambient must be no more than 3.44 C/W | 110 C rise, about 135 C die |

The lesson is not the particular numbers. It is that the ambient and the
interface terms consume margin quickly. A 75 C ambient leaves much less room
than a 25 C bench measurement, and a poor interface can dominate a good
heatsink.

### 3.2 Safe operating area

The SOA curve has four regions: maximum current at low VCE, a thermally limited
region, a second-breakdown region, and breakdown voltage [C222]. The curve is
an absolute maximum rating. Operating on the thermal-limit portion produces the
maximum allowable junction temperature and is not advised for long-term
operation; operating below the limit improves reliability and MTTF [C223].

The most stressful point is usually not maximum output. For a DC resistive
load, peak amplifier dissipation occurs at an output voltage of V+/2, or 50%
output, where `PD = (V+)^2/(4RL)` [C224]. For a sine wave, dissipation reaches a
maximum when the output peaks are about 63% of the supply voltage, because the
instantaneous output remains near half-supply for much of the cycle [C225].

AC signals are generally less demanding than DC signals of the same peak
voltage and current because above about 50 Hz the junction temperature follows
average power, and in a bipolar sine wave each output transistor rests for a
half-cycle [C230]. Do not use that as an excuse to skip the peak check: the
instantaneous peak must still be inside the SOA.

#### Derating and second breakdown

A transistor's maximum dissipation rating applies at a 25 C case and derates
linearly to zero at about 150 C; very few transistors are designed for a
junction temperature above 150 C [C231]. For a 150 C device the derating factor
is the 25 C dissipation divided by 125 C, so a 230 W device derates by
1.84 W/C [C232]. A 230 W transistor may be limited to about 120 W at typical
operating temperatures because the junction-to-ambient resistance is about
1.5-2 C/W even with a large heatsink [C238].

Second breakdown is a localized thermal runaway in a BJT that can destroy the
device in about 10 ms while the case is still cool [C237]. This is why a
steady-state thermal calculation is not enough: a brief excursion into the
second-breakdown region can fail the device before the heatsink responds.

MOSFETs do not suffer second breakdown, but switching (vertical) MOSFETs are
not recommended for linear use; lateral MOSFETs are limited mainly by average
power and can self-limit, although this is not a protection scheme [C239]. The
SOA discussion in this section is for linear output stages; switching devices
have different loss mechanisms and need the manufacturer's switching data.

#### Short circuit

A short to ground forces the full supply across the conducting output
transistor. With +/-40 V, a 3 A current limit is safe only if the case is held
at 25 C and dissipates 120 W; an 85 C case allows 2 A and 80 W with a
0.75 C/W heatsink [C227]. A short to either supply puts the sum of both supply
voltages across the transistor, a more demanding case than a short to ground
[C228].

A foldover current limiter reduces the current limit when VCE is high, but it
can produce unusual behavior with reactive loads [C229]. Foldover is not a
universal solution; test it with the real load.

#### Reactive-load SOA

A purely reactive load can dissipate about three times the worst-case
resistive-load power at full output [C226]. At 45 degree phase, peak
dissipation doubles and load power halves [C235]. ESP's 3 Ohm, 45 degree,
+/-35 V example reaches almost 200 W peak and about 43 W average, with the peak
at the voltage zero crossing [C236]. Check the SOA at that point, not at the
average.

### 3.3 A thermal and SOA procedure

1. **Define the load envelope.** Get impedance magnitude and phase versus
   frequency; use the minimum impedance and the worst phase [C234][C235].
2. **Define the signal.** State crest factor and duty; use a sine for the
   conservative thermal test and the expected programme for the realistic one
   [C259][C246].
3. **Compute peak device stress.** Use instantaneous VCE and current at the
   worst phase, including the high-line supply [C236][C170].
4. **Compare with the SOA at the expected case temperature.** The datasheet
   curve is usually at 25 C; derate it [C231][C232].
5. **Check second breakdown.** Stay out of the second-breakdown region at all
   times, including short faults [C237].
6. **Compute average dissipation.** Use the expected signal and duty, not the
   peak, for the heatsink [C230][C259].
7. **Solve the thermal chain.** Choose `theta-JC`, `theta-CH` and `theta-HA`;
   compute `TJ` at the real ambient [C243][C260].
8. **Check the fault cases.** Short to ground, short to either rail, fan
   failure and DC offset [C227][C228].
9. **Check the drivers.** Driver transistors are exposed to the same SOA limits
   and must be checked too [C266].

## 4. Protection

### 4.1 Principles

Protection is layered. The first layer is enough SOA and thermal margin that
the device is not at its limit in normal use. The second is current limiting
and thermal protection. The third is loudspeaker protection after an amplifier
fault.

Fuses protect against fire and further damage, not the output devices: no fuse
is fast enough to protect a transistor unless it is so low in value that it
blows during normal use [C241]. A fuse is not an SOA limiter. The SOA curve is
an absolute maximum, and protection that operates only after the device is
outside it is not protection [C223].

A protection circuit that switches the output devices off quickly can generate
a destructive flyback voltage from a reactive load. Catch diodes from the
output to each supply clamp the output to the rails [C242]. Check that the
diodes are rated for the fault current and that the layout keeps the return
path short.

### 4.2 Output-stage protection

A typical discrete SOA protection circuit senses current through the emitter
resistors and removes base drive from the driver transistors. It must allow the
high current that a reactive load demands at zero output voltage, which is
close to the short-circuit condition [C240]. That is the hard part: a limiter
tight enough to protect a short may operate on a legitimate reactive load, and
a limiter loose enough for the load may not protect the short.

The short-circuit example shows the trade-off. With +/-40 V and a 25 C case, a
3 A limit is safe but dissipates 120 W; an 85 C case allows 2 A and 80 W with a
0.75 C/W heatsink [C227]. A short to either supply is worse [C228]. If the
amplifier must survive these faults, the heatsink and device count must be
sized for them, or the fault must be cleared quickly by fuses or fault sensing.

Foldover limiting can reduce the current when VCE is high, but it can produce
unusual behavior with reactive loads [C229]. Test it with the real load and
with the expected fault, not only with a resistive dummy.

Few discrete protection circuits monitor output-device temperature or average
power, so a hot amplifier has less protection than a cold one; thermal tracking
is automatic in IC power amplifiers because the devices share one die [C262].
For a discrete design, add a thermal switch or a fan-failure detector, and test
the protection at the highest ambient.

### 4.3 Loudspeaker protection

A shorted output transistor can put a rail voltage across the speaker. A 42 V
DC fault into a 6 Ohm voice coil dissipates about 294 W continuously and can
destroy the driver in seconds [C253]. This is a different failure from
overpowering the speaker with music: there is no cone movement and therefore no
effective cooling.

ESP states that +/-100 mV is generally accepted as the maximum DC offset,
corresponding to 2.5 mW into a 4 Ohm load [C263]. That is a **practitioner
guidance** target, not a standard; confirm the acceptable offset for the
specific driver.

A speaker-protection relay should short the speaker to ground when it operates
rather than simply open the circuit, because a 70 V DC fault can sustain an arc
across opening contacts [C254]. Most common relays are rated 30 V DC at 10 A;
two contact sets in series can interrupt about 60 V DC, and a 70 V DC arc may
require at least 1.6 mm contact clearance [C255]. Above +/-35 V, ESP recommends
a MOSFET relay because an electromechanical relay cannot reliably break the
resulting DC arc [C258]. This relay practice comes from one named practitioner
and is labelled **practitioner guidance**; it needs a second independent source
before it becomes a repository rule.

A DC detector needs a low-frequency filter so legitimate low-frequency signals
do not trip it. ESP uses a 1 Hz single-pole filter and reports that 30 V RMS at
5 Hz does not trigger it while 30 V DC triggers in 60 ms [C256]. For a
full-range system with a 20 Hz low-frequency limit, at least 25 ms of detection
delay is needed to avoid nuisance tripping; practical systems often need more
[C264]. The delay trades protection speed against false trips.

A relay coil driven through a catch diode releases more slowly. ESP measured
1.2 ms without a diode, 7.2 ms with a diode, and 3.5 ms with a diode-resistor
network [C257]. Faster release is not automatically better: the back-EMF from
the coil can destroy the driver transistor if it is not handled [C267]. Use the
manufacturer's recommended coil suppression and measure the release time.

### 4.4 Protection checklist

| Fault | Detection | Actuator | Verification |
|---|---|---|---|
| Output short | Emitter-resistor current sense or supply current | Current limit, foldover or fuse [C240][C229][C241] | Test at high line with a reactive load and a direct short [C227] |
| Sustained overcurrent | SOA-shaped limiter | Remove base drive or mute input [C240] | Check that legitimate 45 degree loads do not trip [C235] |
| Overtemperature | Thermal switch, IC warning flag or case sensor | Fan, shutdown or input mute [C247][C262] | Soak at maximum ambient with the worst signal [C246] |
| DC offset | Low-pass detector | Relay shorts speaker to ground [C254] | Inject both polarities; check trip time and false trips [C256] |
| Fan failure | Airflow or temperature sensor | Shutdown or power reduction | Block the fan at full power |
| Inductive kick | Catch diodes | Clamp output to rails [C242] | Test with a reactive load and abrupt shutdown |

Do not perform destructive arc tests on a real loudspeaker. Use a dummy load
and appropriate test facilities, and treat mains-connected fault testing as
safety-critical work.

## 5. Reactive loads and loudspeaker impedance

The load is not a resistor. A nominal 8 Ohm loudspeaker can fall to 3 Ohm or
less and rise to 50 Ohm or more at resonance, and a nominal 4 Ohm loudspeaker
can have a minimum near 3 Ohm [C234]. At 45 degree phase, peak dissipation
doubles and load power halves [C235]. ESP's 3 Ohm, 45 degree, +/-35 V example
reaches almost 200 W peak and about 43 W average [C236]. A purely reactive load
can dissipate about three times the worst-case resistive-load power at full
output [C226].

The practical consequences:

- **Use the impedance and phase curve**, not the nominal label. If the
  manufacturer does not publish it, measure it or use a conservative minimum
  [C234].
- **Check the SOA at the voltage zero crossing.** That is where current is
  highest while the voltage across the device is also high [C236].
- **Allow the current that the reactive load needs.** A limiter that only
  protects a short may trip on a legitimate load [C240].
- **Do not rely on cable resistance.** It can mitigate the inductive part, but
  it wastes power and changes the load [C265].
- **Check the protection with the real load.** Foldover and other limiters can
  behave unusually with reactive loads [C229].

## 6. Class-D

Class-D amplifiers achieve higher efficiency than Class-AB, but their power
loss is not negligible and needs a PCB or heatsink thermal path; an inadequate
thermal design can trigger thermal protection [C245]. The thermal chain in §3
still applies, but the loss distribution is different: the output devices
switch, and the output filter and PCB also dissipate heat.

Audio thermal tests commonly use sine, pink noise or music. Sine is the most
strenuous and least representative, pink noise better simulates music's
dynamic range, and automotive thermal tests typically use 75-85 C ambient
[C246]. Use the test signal that matches the actual duty; a sine test alone can
overstate or understate the real thermal load depending on the amplifier.

The thermal design limit should be an overtemperature warning threshold rather
than the shutdown threshold, because shutdown interrupts playback [C247]. That
is a Class-D IC example, but the principle applies to any amplifier with a
warning flag: leave room between the warning and the shutdown.

This document does **not** cover Class-D modulator design, dead time, output
filter selection, EMI, feedback or spread-spectrum modulation. Those are
recorded as gaps. The SOA discussion in §3.2 is for linear output stages;
switching devices have different loss mechanisms and need the manufacturer's
switching data.

## 7. Design review and verification

| Check | Method | Evidence to record |
|---|---|---|
| Load envelope | Impedance magnitude and phase versus frequency | Minimum impedance, worst phase, frequency [C234][C235] |
| Output power | RMS voltage and current at clipping, both channels | Load, supply, frequency, distortion limit [C166] |
| Distortion | THD/IMD versus level and frequency, inspect residual | Conditions and residual, not one number [C166] |
| SOA | Instantaneous VCE and current at worst phase and high line | Device, case temperature, SOA curve [C222][C236] |
| Thermal | Thermocouples on case and heatsink, soak at max ambient | Ambient, signal, duration, stabilised temperature [C243][C260] |
| Short circuit | Current-limited fault test at high line | Current limit, duration, device temperature [C227] |
| DC offset | Inject both polarities into the detector | Trip time, false-trip test [C256] |
| Relay | Check DC rating and contact arrangement | Voltage, current, contact clearance [C255][C254] |
| Fan failure | Block airflow at full power | Temperature rise and shutdown behaviour [C262] |
| Inductive kick | Abrupt shutdown into a reactive load | Output clamp and device stress [C242] |

Do not accept a single THD number without its conditions [C166]. Do not accept
a thermal measurement taken only at 25 C ambient if the product will run at
50 C [C260]. Do not accept an SOA check that uses average power; the SOA is an
instantaneous limit [C223].

## 8. Handoff to `circuit-design-skill`

The audio skill supplies the targets, load, supply, ambient and pass/fail
conditions. The circuit skill supplies the netlist, simulator, schematic and
verification report. The handoff contract is in `references/handoff.md`.

For a power stage, the current generic `metrics` stage can verify:

- `gain_db` and `bandwidth_hz` from an AC sweep;
- `thd_percent` from a `.four` analysis at a stated frequency, level and load;
- `output_vrms` from a transient analysis;
- `ein_uv` or `noise_uv` from a noise analysis.

It does **not** compute SOA, junction temperature, thermal resistance or
protection behaviour. Those need the device datasheet curves, a thermal
calculation and a bench test. Send the simulated device voltage and current
waveforms, the operating points and the assumed case temperature; interpret
them against the SOA in this document and the exact datasheet.

State the conditions with every metric: supply, load, frequency, level,
temperature and simulator models. A metric without conditions is not a
verification [C166].

## Sources

All sources below were opened on 2026-11-09. Claim locators are in
`evidence/*.jsonl`.

- [S055] Douglas Self, *Distortion In Power Amplifiers*, updated 12 September
  2019. <http://www.douglas-self.com/ampins/dipa/dipa.htm>
- [S061] Rod Elliott, *Semiconductor Safe Operating Area*, Elliott Sound
  Products, page created 8 August 2003. <https://sound-au.com/soa.htm>
- [S062] Bruce Trump, *Power Amplifier Stress and Power Handling Limitations*,
  Burr-Brown Corporation Application Bulletin AB-039 (SBOA022), April 1993.
  <https://www.ti.com/lit/an/sboa022/sboa022.pdf>
- [S063] onsemi, *Heat Sink Selection Guide*, application note AND9016/D,
  February 2015, Rev. 1.
  <https://www.onsemi.com/download/application-notes/pdf/and9016-d.pdf>
- [S064] Robert Clifton, *Understanding Thermal Capabilities of Automotive
  Class-D Amplifiers*, Texas Instruments application report SLAA996A, June
  2021. <https://www.ti.com/lit/an/slaa996a/slaa996a.pdf>
- [S065] Rod Elliott, *Loudspeaker Protection and Muting*, Elliott Sound
  Products, Project 33, copyright October 1999, updated November 2022.
  <https://sound-au.com/project33.htm>
- [S066] Apex Microtechnology, *Thermal Techniques*, application note AN11,
  October 2012, AN11U Rev G.
  <https://www.apexanalog.com/resources/appnotes/an11u.pdf>

## Unverified and open gaps

- **No Tier 1 or Tier 2 source for power-amplifier thermal design or SOA.**
  The thermal chain, derating and SOA material is Tier 3 practitioner
  guidance. It is corroborated by several independent vendor and practitioner
  sources, but it is not a standard.
- **Loudspeaker protection relay practice** comes from one named practitioner
  [S065]. The recommendation to short the speaker, the 30 V DC relay rating and
  the 1.6 mm clearance figure need a second independent source before they are
  treated as a repository rule.
- **Heatsink orientation** [C251] is from one vendor application note. Verify it
  in the actual enclosure and airflow.
- **Valve (tube) power amplifiers** are not covered: no verified source in the
  registry.
- **Class-D modulator design, dead time, output filter, EMI, feedback and
  spread-spectrum operation** are not covered. The thermal material in §6 is
  not a Class-D design procedure.
- **Long-term thermal cycling, solder fatigue and connector aging** are not
  covered. A steady-state thermal calculation does not predict them.
- **Output-stage distortion beyond Self's measurements** is not covered. The
  numbers in §2 are specific to Self's test conditions and should not be
  generalized.
- **No blind listening evidence** supports claims that one power stage
  "sounds better" than another. Treat such claims as hypotheses.
- **No destructive arc-test procedure** is provided. High-voltage DC fault
  testing is safety-critical and needs the right facilities, not a bench
  improvisation.

See `references/source-gaps.md` for the live list.
