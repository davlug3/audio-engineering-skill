# Small-Signal Audio

This document covers the line-level and low-level part of the signal path:
levels, impedance, gain distribution, buffers, balanced and unbalanced
interfaces, input protection, RF immunity and tone controls. It is a companion
to `analog-design.md`, which covers noise, op-amp selection, distortion
mechanisms and the microphone-preamplifier case study, and to
`grounding-shielding.md`, which covers shields, ground loops and safety.

It does **not** replace simulation, schematic capture or measurement. It gives
the design intent and the conditions that the electrical engine in
`circuit-design-skill` must verify.

Every numeric or behavioural statement carries a claim ID. The claim, its
locator and its source are in `evidence/*.jsonl` and `catalog/sources.json`.
Where a design rule rests on a single practitioner source it is labelled
**practitioner guidance**, and the gap is recorded at the end of this document
and in `references/source-gaps.md`.

## 0. How to use this document

1. Write the interface budget before choosing a part: source impedance, load
   impedance, nominal level, maximum level, bandwidth, gain, noise and
   distortion.
2. Resolve every value against a claim. If no claim exists, write `unverified`
   and add the gap to `references/source-gaps.md`.
3. Choose the interface first: balanced or unbalanced, transformer or active,
   and whether the input must survive phantom-power faults.
4. Choose the gain distribution and the buffer strategy before choosing the
   op-amp. A part that is excellent in one stage can be unstable or noisy in
   another.
5. Send the resulting stage budget to `circuit-design-skill` for AC, noise,
   transient and distortion simulation; see §7 and `handoff.md`.
6. State the conditions with every result: level, frequency, load, gain,
   bandwidth, source impedance and measurement method. A number without its
   conditions is not a specification [C166].

## 1. Levels, impedance and headroom

### 1.1 Reference levels and required conditions

Pro-audio line level is commonly referenced to +4 dBu, and that is the level
used for full-disclosure THD tests [C168]. The reference must be stated; a
signal level in dBu is not a gain and a noise figure in dB is not a level.
S/N conditions are covered in `measurement.md` [C147].

A maximum output specification must state whether the output is balanced or
unbalanced, the distortion criterion, the frequency range and the guaranteed
load impedance [C191]. A maximum input specification must state balanced or
unbalanced operation and the distortion criterion; 1% THD is the preferred
criterion, while "visible clipping" can be as much as 10% distortion [C154].

Input and output impedance must state balanced or unbalanced operation and
whether the port is floating or ground-referenced [C155]. Two inputs with the
same nominal impedance can therefore describe different circuits: one may be
that impedance from each line to ground, the other that impedance between the
two lines.

A maximum gain specification is measured with all level and gain controls at
maximum, using a 1 kHz input that does not clip the output, and it must state
whether the output is balanced or unbalanced [C220].

**Practitioner guidance:** use +4 dBu as the pro-audio reference and state the
consumer or instrument level separately. Do not mix specifications made at
different reference levels without converting both to the same reference.

### 1.2 Impedance bridging without a universal ratio

Input impedance is the load that a unit presents to the driving source; output
impedance is the source impedance that drives the next unit [C155]. About
1 kOhm is a fair estimate of the average output impedance of typical signal
sources, and a 1 kOhm resistor has a thermal-noise density of about
4 nV/sqrt(Hz) [C022]. That noise matters when the source impedance is high;
see `analog-design.md` §2.

Load drive is a separate constraint from noise. Driving a 600 Ohm load calls
for an op-amp rated for the purpose, such as an NE5532/4, LM4562 or OPA2134;
a high-impedance source calls for a JFET-input op-amp [C023]. The JFET-input
TL072 has higher voltage noise than bipolar audio op-amps but outperforms them
with a high-impedance source [C024].

A 4580 can drive a 200 Ohm load at no more than 1 V peak without showing
increased distortion [C213]. That is a useful data point, not a general
guarantee: the allowable load depends on the part, the output swing, the
supply voltage and the distortion criterion. Check the datasheet's load-drive
graph at the actual worst-case swing.

**Practitioner guidance:** the common "10:1 bridging rule" is **unverified**
in this repository; it is a starting point, not a specification. For
line-level outputs, a load of 2 kOhm or greater is preferred, and 600 Ohm
operation is obsolete except for specialized broadcast and telecommunications
applications [C192]. For a high-impedance instrument source, the input
impedance must be set from the source and cable capacitance, not from a
generic ratio.

Long unbalanced cables amplify the side effects of unbalanced ground loops;
keep any unbalanced cable under ten feet (three metres) [C113]. A balanced
interface is the better choice for longer runs; see §3.

### 1.3 Headroom and gain distribution

Headroom is the difference between the nominal operating level and the
maximum output level. Both must be stated with the same reference and the same
load [C191]. A +4 dBu nominal level with 15 dB of headroom and an 80 dB
interface CMRR gives 95 dB of total dynamic range, comparable to a CD; 50 dB
of CMRR is rarely enough for a commercial system [C123].

A line-input attenuator trades input impedance against noise and headroom.
More attenuation provides more headroom, while a lower input impedance lowers
the noise floor [C195][C196]. At -6 dB system gain, a THAT 1512 line input
accommodates +27.5 dBu, has -100 dBu input-referred noise and 127.5 dB dynamic
range [C196]. These are the kind of conditions that must be quoted together;
the headroom number alone is not comparable with a different input impedance
or gain.

Few power amplifiers need more than about +4 dBV (1.58 V RMS) input for full
power. A preamplifier that can deliver 5-6 V RMS will drive any amplifier;
this is easily achieved with +/-12 V supplies, although +/-15 V is usually
preferred [C199]. Two 10 dB gain stages provide about 20 dB, enough for a
preamplifier stage while allowing for the losses of volume and balance controls
[C198].

**Practitioner guidance:** distribute gain in stages of roughly 10 dB where
possible. It keeps each stage's noise gain, bandwidth and clipping point
manageable, and it leaves room for the losses of controls and passive
networks. The exact distribution is a simulation and measurement question, not
a rule.

## 2. Gain blocks and buffers

### 2.1 Gain staging

Gain is not a single number: it is defined at a frequency, a level and a load,
with a tolerance. A frequency-response specification should be stated as a
tolerance, for example 20 Hz to 20 kHz +0/-0.5 dB [C152]. The same discipline
applies to a gain block: state the gain at 1 kHz or over the band, the source
impedance, the load and the output level.

An inverting stage at unity signal gain has a noise gain of 2 because the input
and feedback resistors contribute; low-noise designs therefore usually use the
non-inverting topology [C007]. In a non-inverting amplifier the noise gain is
1 + Rf/Rg, and each noise source is multiplied by its gain to the output
before RMS summation [C018]. This is why a low-noise first stage should not be
an inverting summing stage unless the summing function is essential.

Op-amp selection should consider circuit type, required speed, load drive,
signal level, noise, supply voltage, package and cost; unsupported claims
about "sound" are not selection criteria [C020]. ESP's compiled typical
datasheet values include AD797 0.9 nV/sqrt(Hz), 110 MHz and 20 V/us; LT1115
0.9 nV/sqrt(Hz), 70 MHz and 15 V/us; OPA1612 1.1 nV/sqrt(Hz), 40 MHz and
27 V/us; LM4562 2.7 nV/sqrt(Hz), 55 MHz and 20 V/us; NE5532 5 nV/sqrt(Hz),
10 MHz and 9 V/us; TL072 18 nV/sqrt(Hz), 3 MHz and 13 V/us; and uA741
23 nV/sqrt(Hz), 1 MHz and 0.5 V/us [C021].

Slew rate must be checked against the required full-power bandwidth rather
than assumed from the part's reputation. A 741 with a 0.5 V/us slew rate can
still deliver about 3 V RMS at 20 kHz [C025]. The check is:

- required peak output voltage;
- required frequency;
- required slew rate = 2 pi f Vpeak;
- the op-amp's datasheet slew rate with margin.

The bass response of an op-amp circuit is determined by passive components,
almost always capacitors; the op-amp itself has no effect on bass response
[C215]. ESP measured all audio-grade op-amps flat from DC to at least 100 kHz
(+/-0.1 dB) in a 10 dB gain circuit [C214]. Choose an op-amp for noise, load
drive, stability and distortion, not for a "bass character".

### 2.2 Buffers and load drive

A buffer provides no voltage gain. Its job is to present a high input
impedance to a high-impedance source and a low output impedance to a low-Z
load. Tone-control networks require a low or very low impedance source and a
high impedance load; input buffers are essential even when the input uses an
inverting op-amp stage, because insertion loss depends on source impedance
[C205].

A unity-gain buffer is not automatically stable with every op-amp. The NE5534
is stable only at a gain of three or more unless an external compensation
capacitor is added, and it can oscillate in a unity-gain circuit [C200]. Check
the datasheet's minimum stable gain before using a part as a follower, and
check the load capacitance and output swing.

The output stage must be able to drive the actual load at the actual swing.
A 600 Ohm load calls for an op-amp rated for the purpose [C023]. A 4580 can
drive 200 Ohm at up to 1 V peak without increased distortion [C213], but a
different part or a higher swing may not. Verify output swing, distortion and
thermal rise at the worst-case load.

### 2.3 Gain-block checklist

- Source impedance and load impedance, including cable capacitance [C155].
- Required gain and frequency-response tolerance [C152].
- Maximum input level and maximum output level, with the distortion
  criterion [C154][C191].
- Noise: EIN, source impedance and bandwidth; see `analog-design.md` §2
  [C045][C046].
- Distortion at the actual level, load and gain [C166].
- Stability: minimum stable gain, capacitive load and compensation [C200].
- Supply voltage, package and thermal rise [C020].
- Simulate and measure the completed stage, not just the ideal gain equation.

## 3. Balanced and unbalanced interfaces

### 3.1 What "balanced" means

A balanced line has two signal conductors plus a shield [C109]. AES48
specifies balanced lines with the cable shield tied to the metal chassis at
both ends [C109]. XLR pin 1 should be tied to the chassis at the point of
entry, not to the audio signal ground [C110].

Balance is not "two equal and opposite signals". A balanced circuit is a
two-conductor circuit in which both conductors and all connected circuits have
the same impedance with respect to ground and to other conductors, so noise
pickup is common-mode and can cancel in the load [C118]. A balanced interface
rejects noise through common-mode impedance balance, not through equal-and-
opposite signal voltages; this is the definition in IEC 60268-3 [C117].

CMRR is the ratio of differential-mode signal gain to common-mode noise gain,
is expressed in dB, and is not a signal level, so it must not be written as
dBu, dBV or dBm [C120]. Common-mode voltage has three main sources: a voltage
difference between driver and receiver grounds, magnetic-field induction in
the cable, and electric-field induction in the cable [C119].

Real-world common-mode impedances are imbalanced by about +/-10 Ohm at 60 Hz,
and the CMRR of the SSM-2141 receiver drops by 25 dB with only 1 Ohm of driver
imbalance [C122]. A balanced interface behaves as a Wheatstone bridge;
rejecting ground noise requires a precise ratio match of the positive and
negative common-mode divider arms [C121].

### 3.2 Receivers, transmitters and matching

A laser-trimmed differential amplifier such as the THAT 1246 or 1286 provides
typically 90 dB common-mode rejection; the untrimmed 1256 or 1296 provides
typically 50 dB [C193]. A discrete-resistor difference amplifier's common-mode
rejection is limited by resistor matching: 1% resistors give worst-case CMR as
low as 31.5 dB, 0.1% gives 51.5 dB, and matching the laser-trimmed 1246/1286
requires at least 0.01% [C194].

Line-input impedance is a tradeoff: lower impedance lowers the noise floor,
while higher impedance preserves common-mode rejection when the differential
sources have slightly different low output impedances [C195]. It is not a
free choice; state the source impedance and the CMRR target together.

A balanced U-pad changes its attenuation when the source switches from
balanced to unbalanced, while two L-pads maintain the same attenuation for
either source type [C197]. If the input must accept both balanced and
unbalanced sources at the same gain, use the two-L-pad arrangement or a
transformer, and verify the common-mode range.

A differential-to-single-ended converter removes the common-mode signal, while
a balanced output can be made with cross-connected differential amplifiers
[C216]. For a single-ended output, a laser-trimmed line receiver gives high
CMRR; for a balanced output, the cross-connected stage must be checked for
stability and load drive, not just gain.

### 3.3 Unbalanced interfaces

Any unbalanced cable should be kept under ten feet (three metres); longer
cables amplify the side effects of unbalanced ground loops [C113]. A ground
loop is formed when two units' signal grounds are tied together in more than
one place, for example by the signal cable and by the safety earth; hum occurs
when the resulting current flows through a unit's audio signal ground [C108].

Transformer isolation is the most reliable way to break a ground loop between
balanced and unbalanced equipment [C111]. If a shield must be lifted,
disconnect it at the receiving end and capacitively couple it to the chassis
with 0.1 uF or 0.01 uF; this is the hybrid shield termination [C112].
Ground-lift switches are band-aids: in most cases they do not improve ground
noise and they reduce the unit's ability to be properly grounded [C114].

Safety grounding must never be defeated to solve a noise problem; doing so is
dangerous, illegal in many jurisdictions, and creates liability [C126]. NEC
2008 Articles 250.6(D) and 250.114 prohibit removing safety grounding from
plug-and-cord-connected equipment to solve noise issues; signal cables are not
safety-ground wiring [C127]. See `grounding-shielding.md` for the full
treatment.

## 4. Input protection and RF immunity

### 4.1 Phantom-power faults

Phantom-power faults can apply -48 V to a preamplifier input; protection
requires series resistors, diode clamps and capacitors that absorb charge
[C040]. Phantom feed resistors should be thin film, matched to 1% or better,
and rated for the shorted-input dissipation of 0.338 W each [C043].

A 20 dB balanced U-pad can keep the input impedance near 2 kOhm and reduce
resistor matching errors; a bipolar-input preamplifier should see a
differential source impedance no higher than about 2 kOhm [C041].

When two microphone preamps are multed, only one preamp's phantom power should
be on; type A switching halves the phantom voltage because of the off
preamp's DC load, so types B and C are recommended for mults [C217]. The
protection network must survive the fault before the phantom switch is opened,
not just the normal operating voltage.

### 4.2 RF immunity

High-gain preamplifiers can rectify radio frequencies, causing audible
interference [C218]. RF immunity is improved by capacitors at the input
connector returned to the connector shield, plus a third capacitor to shunt
differential RF inside the enclosure [C042]. RF bypass capacitors should be
returned to the connector shield with the shortest possible path [C219]. THAT
Design Note 140 also suggests a common-mode choke as part of the RFI network
[C212].

The layout matters as much as the schematic: the capacitor ground return must
not share a long trace with the audio signal return, and the input wiring
before the connector should be short. A capacitor placed after a long
unshielded lead protects the op-amp but leaves the lead as an antenna.

### 4.3 Overvoltage and ESD

Phantom-power protection is not a general ESD or line-overvoltage design.
There is no verified source in this repository for a complete ESD/line
overvoltage procedure; use the device datasheet's absolute maximum ratings,
the connector's intended environment and the applicable safety standard. Do
not infer a mains-fault rating from a phantom-protection network.

### 4.4 Pads and line inputs

A 20 dB balanced U-pad can keep the input impedance near 2 kOhm and reduce
resistor matching errors; a bipolar-input preamplifier should see a
differential source impedance no higher than about 2 kOhm [C041]. A balanced
U-pad changes its attenuation when the source switches from balanced to
unbalanced, while two L-pads maintain the same attenuation for either source
type [C197].

A line-input attenuator with more attenuation provides more headroom, while a
lower input impedance lowers the noise floor [C195][C196]. At -6 dB system
gain a THAT 1512 line input accommodates +27.5 dBu, has -100 dBu input-referred
noise and 127.5 dB dynamic range [C196]. Check that the pad's resistor
tolerance and the source's output impedance do not degrade CMRR below the
system target.

## 5. Tone controls and equalisers

### 5.1 Reproduction versus production

In hi-fi or mixing-console use, it is essential that a flat response is
available with the boost/cut controls centred; the circuit then has no effect
on the response [C203]. A guitar tone stack is different: it is part of the
instrument and the loudspeaker system, it has no true flat setting, and it
produces a midrange scoop [C203].

Simple RC tone-control circuits have a theoretical maximum slope of
6 dB/octave [C204]. Steeper slopes require LC, gyrator, active-filter or DSP
techniques, and each has its own stability, noise and distortion tradeoffs.

### 5.2 Passive and active topologies

A passive James or Baxandall bass and treble control has about 20 dB insertion
loss, so a gain of 10 is needed to restore the level with the controls set for
nominally flat response [C201]. A passive Baxandall or James tone control also
has a flat-response error of up to about +/-2 dB and interactive controls, so
a true flat position is difficult to achieve [C208].

An active Baxandall tone control requires an inverting amplifier stage with
low output impedance to drive the filter network, and gives approximately
symmetrical boost and cut; with the values shown in the source, the maximum is
about +/-15 dB [C202]. A three-band Baxandall tone control has a Q of about
0.5, so it cannot make a narrow midrange correction [C207].

Tone-control circuits require a low or very low impedance source and a high
impedance load; input buffers are essential even when the input uses an
inverting op-amp stage, because insertion loss depends on source impedance
[C205]. For a tone-control network, doubling the capacitance halves the
frequency; changing the capacitance by a factor of 1.5 changes the frequency
by the same fraction [C209].

### 5.3 Guitar tone stacks

A guitar tone stack has no true flat setting, produces a midrange scoop, and
has insertion loss of about 8 dB for a Marshall-style stack to about 15 dB for
a Fender-style stack with the controls centred [C203]. The midrange control
only reduces the depth of the notch, the notch frequency varies with control
settings, and the controls are interactive [C210]. The Fender-style stack has
more bass and treble boost and a deeper notch than the Marshall-style stack;
the notch varies from about 300 Hz to 1 kHz for both [C211].

A guitar tone stack is not a hi-fi equaliser. Use it for instrument voicing,
not for flat-response monitoring or room correction. If a flat response is
required, use a bypassable active EQ or DSP.

### 5.4 Graphic and parametric equalisers

A graphic equalizer can have a Q that varies with boost and cut, or a constant
Q; the constant-Q design sums band-pass filter outputs and keeps the filter
loading constant [C206]. The variable-Q type is simpler but its bandwidth
changes with the slider setting; the constant-Q type is more predictable for
repeatable corrections.

A three-band Baxandall tone control has a Q of about 0.5, so it cannot make a
narrow midrange correction [C207]. For narrow corrections, use a peaking or
parametric filter, or DSP. The repository does not yet have a verified source
for a complete analog parametric-EQ design procedure; record that as a gap if
you need one.

### 5.5 Tone-control checklist

- Define the target response, the tolerance and the reference level [C152].
- Choose passive or active from the insertion loss you can afford
  [C201][C202].
- Buffer the input and output; the network needs a low source impedance and a
  high load [C205].
- Check the boost/cut range and the flat-position error [C202][C208].
- Check noise gain and clipping at maximum boost [C007][C166].
- Simulate the potentiometer at its worst-case settings, not just at centre.
- Measure the completed circuit with the actual pots, capacitors and load.

## 6. Layout and wiring checklist

- Put RF bypass capacitors at the input connector and return them to the
  connector shield with the shortest possible path [C042][C219].
- Tie XLR pin 1 to the chassis at the point of entry, not to the audio signal
  ground [C110].
- Keep unbalanced cables under three metres [C113].
- Separate signal and power bundles by at least 6 inches for unbalanced
  interfaces [C129].
- Use star grounding or a mesh ground plane; mesh grounding approximates a
  ground plane at high frequencies and tolerates loops, while star grounding
  avoids shared conductors and is preferred for audio because 60 Hz is in
  band [C130].
- Take the power-supply earth reference at the output/regulator end, not at
  the rectifier [C136].
- Never defeat the safety earth to solve a noise problem [C126][C127].
- Bypass each op-amp close to its supply pins, and check the minimum stable
  gain of the part [C200][C221].
- Verify the completed unit with the real source, cable and load; a
  simulation without cable capacitance and connector impedance is incomplete.

## 7. Handoff to `circuit-design-skill`

The handoff is the contract between this document and the electrical engine.
Use the fields in `handoff.md`:

- `gain_db` for the stage gain at a stated frequency and load;
- `bandwidth_hz`, `bandwidth_low_hz` and `bandwidth_width_hz` for the
  frequency limits;
- `ein_uv` for the input-referred noise at the stated source impedance and
  bandwidth;
- `thd_percent` for the distortion at the stated level, frequency, gain and
  load;
- `output_vrms` for the maximum output before the stated distortion criterion.

Every metric needs the analysis and the test point that the circuit skill will
use. The merge adds `analysis`, `output`, `input` and the matching analysis
entry; see the circuit skill's `references/audio-handoff.md`. Do not put a
part number in the handoff unless its datasheet source is recorded.

## Sources

All sources below were opened on 2026-11-08. Claim locators are in
`evidence/*.jsonl`.

- [S040] Dennis Bohn, *RaneNote 110: Sound System Interconnection*, Rane
  Corporation, revised 2017.
  <https://www.ranecommercial.com/legacy/note110.html>
- [S041] Dennis Bohn, *RaneNote 145: Audio Specifications*, Rane Corporation,
  written 2000, revised 1/03.
  <https://www.ranecommercial.com/legacy/note145.html>
- [S045] Rod Elliott, *Noise in Audio Amplifiers*, Elliott Sound Products,
  copyright 1999, updated May 2025. <https://sound-au.com/noise.htm>
- [S047] Rod Elliott, *Opamp Selection*, Elliott Sound Products, September
  2025. <https://sound-au.com/articles/opamp-selection.htm>
- [S048] Rod Elliott, *Earthing (Grounding) Your Hi-Fi: Tips, Tricks and
  Techniques*, Elliott Sound Products. <https://sound-au.com/earthing.htm>
- [S049] Texas Instruments, *Noise Analysis in Operational Amplifier Circuits*
  (SLVA043B). <https://www.ti.com/lit/pdf/slva043>
- [S053] Bill Whitlock, *An Overview of Audio System Grounding & Interfacing*,
  presentation slides, 9/4/2012.
  <https://jhbrandt.net/assets/resource/An_Overview_of_Audio_SystemGrounding_and_Interfacing.pdf>
- [S054] THAT Corporation, *Input and Output Circuits for THAT Preamplifier
  ICs* (Design Note 140), Doc 600140 Rev 03, copyright 2011-2014.
  <https://thatcorp.com/datashts/dn140.pdf>
- [S055] Douglas Self, *Distortion In Power Amplifiers*, updated 12 September
  2019. <http://www.douglas-self.com/ampins/dipa/dipa.htm>
- [S060] Rod Elliott, *Equalisers, The Various Types And How They Work*,
  Elliott Sound Products, copyright March 2015, updated February 2021.
  <https://sound-au.com/articles/eq.htm>

## Unverified and open gaps

- The "10:1 impedance bridging" rule is not supported here by a standard or
  peer-reviewed source. This document uses the source/load definitions and
  the 2 kOhm preferred-load guidance instead [C155][C192].
- ESD and line-overvoltage protection for small-signal inputs have no verified
  procedural source. Phantom-fault protection is covered [C040], but it is
  not a general overvoltage design.
- Mains safety isolation of small-signal inputs is not covered here; refer to
  the power-supply and safety material.
- The tone-control claims are Tier 3 practitioner guidance from ESP. There is
  no peer-reviewed listening-test or tolerance study in the registry, and the
  source's circuits were simulated but not built as shown [S060].
- Active-filter Q, component selection and stability for parametric EQ are not
  covered by a verified source. Use circuit simulation and the filter
  literature before claiming a design.
- Capacitor distortion in tone and coupling networks is not covered here; see
  `analog-design.md` and the capacitor-distortion claim [C048].
- Balanced output stage stability, load drive and short-circuit protection are
  not covered by a verified source. The cross-connected topology is described
  [C216], but the design procedure is not.
- Potentiometer law, tolerance and tracking effects on tone-control flatness
  are only partly covered by the practitioner source [C208].
- Digital equalisation, DSP and room correction are outside this document.
- Transformer selection for input/output isolation (turns ratio, shielding,
  leakage inductance, saturation) is not covered by a verified source.

See `references/source-gaps.md` for the live list.
