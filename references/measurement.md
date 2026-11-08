# Measurement

An audio measurement is a number plus the conditions that make it meaningful.
This document defines the tests, the conditions that must accompany them, and
the traps that make a plausible-looking specification worthless. It is the
reference for the `metrics` handoff to `circuit-design-skill`: the circuit
skill produces the simulation data, and this document says how to turn it into
a claim that can be compared with a measurement.

Every numeric or behavioural statement carries a claim ID. Claims are in
`evidence/*.jsonl`.

## 0. Principles

1. **State the conditions.** A THD or THD+N number without test frequency,
   level, gain, load and bandwidth is not a specification [C166].
2. **Measure the residual, not just the number.** A single THD value can hide
   crossover spikes, hum, RF or noise. Inspect the residual waveform and
   spectrum.
3. **Know the floor.** The measurement system's own noise and distortion set
   the floor; at very low distortion levels the residual is mostly noise
   [C167].
4. **Use a sine for THD.** A sine has a single known fundamental, so any added
   component is measurable; a complex signal makes the residual harder to
   interpret [C165].
5. **Use the right weighting.** A-weighting can hide hum; ITU-R 468 correlates
   better with hearing [C148][C149].
6. **Do not compare numbers measured at different conditions.** This is the
   most common error in audio specifications.

## 1. Distortion

### 1.1 THD

THD is the ratio of the RMS voltage of the harmonics to that of the
fundamental, obtained by measuring each harmonic and RMS-summing them, then
dividing by the fundamental and expressing the result in percent [C142]. The
conditions are the test frequency, its level, the gain setting and the number
of harmonics measured [C142].

A full-disclosure THD specification sweeps 20 Hz to 20 kHz at +4 dBu with the
fifth harmonic or higher measured; for signal processing the preferred gain is
unity, and for microphone preamps maximum gain [C168]. A single 1 kHz number is
a screening test, not a specification.

Percentage and decibels are related by:

| THD | Relative level |
|---|---|
| 1% | -40 dB |
| 0.1% | -60 dB |
| 0.01% | -80 dB |
| 0.001% | -100 dB |
| 0.0001% | -120 dB |

The table is from ESP's conversion chart [C162]. The `dB` column is the
residual relative to the fundamental, not a signal level in dBu.

### 1.2 THD+N

THD+N is the RMS summation of all output components except the fundamental
over a prescribed bandwidth, typically 22 kHz, 30 kHz or 80 kHz, after
removing the fundamental with a notch filter [C143]. It is always a larger
number than THD because it includes noise and other artifacts in addition to
harmonics [C144].

The bandwidth must be stated. An 80 kHz measurement is useful during design and
manufacturing to reveal high-frequency artifacts, while 22 kHz flat is a
defensible published condition [C157]. A 30 kHz bandwidth is also common
[C143].

The notch depth sets the low-distortion limit. A 40 dB notch cannot measure
below 1% distortion, and a 100 dB notch cannot measure below 0.001%, because
residual fundamental leaks through the notch [C163]. If you need to measure
below 0.01% THD+N, the residual is often dominated by noise rather than
distortion [C164], and the notch, the analyzer and the source all matter.

### 1.3 IMD

SMPTE IMD uses 60 Hz and 7 kHz tones in a 4:1 amplitude ratio (12 dB) and
measures the modulation sidebands on the high tone [C145]. ITU-R (formerly
CCIF) IMD uses two equal-amplitude tones spaced 1 kHz apart, commonly 13/14 kHz
or 19/20 kHz, and usually only the first two or three intermodulation
components are measured [C146].

IMD is often more revealing than THD because it exercises the amplifier with a
complex waveform and exposes thermal and bias modulation that a single sine
does not. Report the tone frequencies, the ratio, the level and the order of
the products measured.

### 1.4 Test-frequency limits

The IEC view is that THD should not be tested above 6 kHz when measuring five
harmonics with a 30 kHz bandwidth, or above 10 kHz when measuring the first
three harmonics [C156]. The reason is simple: if the measurement bandwidth does
not include the harmonics, the number is not THD. A 20 kHz THD number measured
with a 22 kHz bandwidth is mostly the second harmonic, not the fifth.

### 1.5 Reading a distortion plot

Crossover distortion occurs over a small part of the transfer characteristic,
generates high-order harmonics, and is present at all output levels; the THD
percentage can rise as output level falls [C028]. A THD-versus-level sweep that
only reports full power can miss it. Plot THD against level from well below the
normal listening level to clipping, and inspect the residual at the crossover
region.

A rising THD at high frequency can be an input-stage or switchoff mechanism,
not a slew-rate limit [C037][C034]. A third-harmonic rise at low load impedance
can be large-signal nonlinearity or beta droop [C031][C032]. The shape of the
curve is diagnostic; the single number is not.

Conventional THD and IMD are also not a complete description of nonlinearity.
A 2026 JAES paper shows that some distortion contributions coincide with the
fundamental frequencies and are therefore missed by conventional metrics, and
proposes a parallel Wiener-Hammerstein measurement to estimate them [C186].
Treat a THD number as one view of the distortion, not the whole model.

### 1.6 Distortion test plan

| Test | Condition | What to record |
|---|---|---|
| THD sweep | 20 Hz-20 kHz, +4 dBu, unity gain (max for mic preamp), 5th harmonic or higher | THD vs frequency, residual spectrum [C168] |
| THD vs level | 1 kHz and 10 kHz, -60 dBu to clipping | THD vs level, crossover region [C028] |
| THD+N | 20 Hz-20 kHz, +4 dBu, 22 kHz flat | THD+N vs frequency, noise floor [C157] |
| SMPTE IMD | 60 Hz/7 kHz, 4:1, +4 dBu (60 Hz) | Products and percentage [C145] |
| ITU-R IMD | 13/14 kHz or 19/20 kHz, 1:1, +4 dBu | First two or three products [C146] |
| Residual | Worst-case frequency and level | Oscilloscope/FFT screenshot, not just a number |

## 2. Noise

### 2.1 S/N

S/N is measured with no signal but with the input terminated, using an RMS
voltmeter and a stated bandwidth; 22 kHz flat is the most common condition
[C147]. The reference level must be stated: a signal-to-noise ratio is
meaningless without it.

A-weighting rolls off low frequencies, reducing the second and third line
harmonics by about 20 dB and 12 dB, and can improve a noise specification by
about 10 dB, hiding hum [C148]. The ITU-R 468 weighting filter correlates
better with hearing than A-weighting and adds about 12 dB of gain in the
critical midband [C149]. Use 468 when you want a number that tracks audibility;
use flat 22 kHz when you want a reproducible engineering number; state which.

### 2.2 EIN

EIN is measured at maximum gain with the input terminated by the expected
source impedance; the standard source impedance is 150 Ohm [C045]. A 150 Ohm
source at room temperature has a thermal-noise limit of -131 dBu over 20 kHz
and -134 dBu over 10 kHz; noise falls by 3 dB when the bandwidth is halved
because voltage is a square-root function [C046].

The EIN measurement is the most useful single noise figure for a microphone
preamp because it includes the gain and the input stage. It is also easy to
fake: a lower gain, a different source impedance or a weighted measurement can
make the number look better. Record the gain, source impedance, bandwidth and
weighting.

### 2.3 Dynamic range

Dynamic range is the ratio of maximum output to the noise floor, with the
reference level and noise bandwidth stated [C150]. It is not the same as S/N:
S/N uses a nominal reference level, while dynamic range uses the maximum output
before clipping. State which one you mean.

### 2.4 Noise measurement procedure

1. Terminate the input with the expected source impedance (150 Ohm for a mic
   preamp, 200 Ohm or 600 Ohm for a line stage as appropriate) [C045].
2. Set the gain to the condition being specified: maximum for EIN, unity for a
   line stage [C168].
3. Measure RMS over a defined bandwidth, flat or weighted [C147][C149].
4. Measure the analyzer's own floor with a shorted input and subtract it in
   RMS, or ensure it is well below the device under test.
5. Check for mains hum and its harmonics; A-weighting can hide them [C148].
6. Report the result in dBu or dBV, with the reference and bandwidth.

## 3. Frequency response and stability

Frequency response should be stated as a tolerance, for example 20 Hz to
20 kHz +0/-0.5 dB; a response that rises with frequency indicates instability
in solid-state equipment [C152]. A "20 Hz-20 kHz" claim without a tolerance is
not a specification.

Measure at more than one level. A small-signal sweep can look flat while a
large-signal sweep shows compression or slew limiting. A square-wave test is a
quick stability check, but it is not a substitute for a loop-gain simulation;
record the overshoot, ringing and settling.

## 4. CMRR and crosstalk

### 4.1 CMRR

CMRR is the ratio of differential-mode signal gain to common-mode noise gain,
is expressed in dB, and is not a signal level, so it must not be written as
dBu, dBV or dBm [C120]. It is measured by driving both inputs through two
equal, carefully matched resistors of half the expected source resistance, and
the test frequency must be stated [C153].

The interface CMRR is not the receiver's advertised CMRR. Real-world
common-mode impedances are imbalanced by about +/-10 Ohm at 60 Hz, and the
CMRR of the SSM-2141 receiver drops by 25 dB with only 1 Ohm of driver
imbalance [C122]. Measure with the actual driver and cable, at 60 Hz and at
1 kHz, and report both. With +4 dBu reference level, 80 dB of interface CMRR
and 15 dB of headroom give 95 dB of total dynamic range; 50 dB is rarely enough
[C123].

### 4.2 Crosstalk

Crosstalk is measured with one channel driven and the other terminated;
capacitive coupling makes it rise at about 6 dB/octave with frequency, so the
test frequency must be stated [C151]. A -60 dB specification at 1 kHz implies
about -36 dB at 16 kHz if the 6 dB/octave trend continues [C151]. Measure at
1 kHz and at 16 kHz, with the undriven channel terminated in its normal load.

### 4.3 Input and output impedance

Input and output impedance must state balanced or unbalanced and whether the
port is floating or ground-referenced [C155]. A "10 kOhm input" claim without
those conditions is incomplete. Measure the impedance at the frequency of
interest; a capacitor-coupled input changes with frequency.

## 5. Maximum levels and headroom

Maximum input level must state balanced or unbalanced and the distortion
criterion; the preferred criterion is 1% THD, while "visible clipping" can be
as much as 10% distortion [C154]. A maximum input specified as "visible
clipping" can therefore be quoted at a higher level than a 1% criterion would
allow.

For a power amplifier, state the maximum output at the specified load and
distortion, the supply voltage, and the duration. For a preamp, state the
maximum input and output at the specified gain. Headroom is the difference
between the nominal level and the clipping point; +4 dBu is 1.23 V [C123].

## 6. Loudness and true peak

ITU-R BS.1770 specifies algorithms for determining subjective programme
loudness and true-peak signal level [C158]. The loudness algorithm uses
K-weighting, per-channel mean square, channel-weighted summation with the LFE
channel excluded, and 400 ms gating blocks overlapped by 75% [C159]. It applies
an absolute gate at -70 LKFS and a relative gate at -10 dB below the level
measured after the absolute gate [C159].

LKFS means loudness, K-weighted, relative to nominal full scale; a 0 dBFS
997 Hz sine on the left, centre or right channel reads -3.01 LKFS [C160]. The
-3.01 dB offset is not a bug: the K-weighting filter has gain at 997 Hz, and
the constant in the loudness equation cancels it [C160].

Use BS.1770 for programme loudness, not for peak level. Use true-peak
measurement for clipping: true peak is the maximum value in the continuous-time
waveform and may be higher than the largest sample value, so a peak-sample
meter can under-read [C181]. Do not substitute A-weighting for K-weighting;
they answer different questions [C148][C159].

## 7. Measurement plan template

| Test | Condition | Instrument | Pass/fail | Evidence |
|---|---|---|---|---|
| THD | 20 Hz-20 kHz, +4 dBu, unity/max gain, 5th harmonic | Audio analyzer or FFT | Budget | Plot and residual |
| THD vs level | 1 kHz and 10 kHz, -60 dBu to clip | Audio analyzer | No crossover rise | Plot |
| THD+N | 22 kHz flat, +4 dBu | Audio analyzer | Budget | Number and bandwidth |
| SMPTE IMD | 60 Hz/7 kHz, 4:1 | Audio analyzer | Budget | Products |
| ITU-R IMD | 19/20 kHz, 1:1 | Audio analyzer | Budget | Products |
| S/N | Input terminated, 22 kHz flat | RMS meter/FFT | Budget | Reference and bandwidth |
| EIN | Max gain, 150 Ohm, 20 kHz | RMS meter/FFT | Budget | Gain and source |
| Frequency response | 20 Hz-20 kHz, +0/-0.5 dB | Sweep | Tolerance | Plot |
| CMRR | 60 Hz and 1 kHz, matched half-source | Audio analyzer | >=80 dB | Driver and cable |
| Crosstalk | 1 kHz and 16 kHz, channel terminated | Audio analyzer | Budget | Both frequencies |
| Max input | 1% THD, balanced | Audio analyzer | Budget | Criterion and gain |
| Max output | Specified load, 1% THD | Audio analyzer | Budget | Load and duration |
| PSRR | Ripple at 100/120 Hz and 1 kHz, actual load | Injection + FFT | Budget | Frequency and headroom |
| Loudness | BS.1770, programme material | Loudness meter | Target | LKFS and true peak |

## 8. Handoff to `circuit-design-skill`

Send the test conditions, not just the netlist. The circuit skill should run:

- `op` for the operating point and device dissipation;
- `ac` for gain, phase margin and bandwidth;
- `noise` for input-referred noise over the specified bandwidth;
- `tran` for large-signal, slew and clipping behaviour;
- `tf` for transfer functions where useful;
- `.four` or an external FFT for THD, once the metrics stage exists.

The current circuit skill does not emit `.four` and its ASCII raw parser cannot
represent AC complex pairs or multi-variable rows correctly. Until that is
fixed, export the raw data and compute the metrics with the definitions in this
document. Do not accept a simulator's "THD" number without the test frequency,
amplitude, load and harmonic count [C166].

## Sources

All sources below were opened on 2026-11-08. Claim locators are in
`evidence/*.jsonl`.

- [S001] International Telecommunication Union, *Recommendation ITU-R
  BS.1770-5: Algorithms to measure audio programme loudness and true-peak
  audio level*, November 2023. <https://www.itu.int/rec/R-REC-BS.1770>
- [S041] Dennis Bohn, *RaneNote 145: Audio Specifications*, Rane Corporation,
  written 2000, revised 1/03.
  <https://www.ranecommercial.com/legacy/note145.html>
- [S046] Rod Elliott, *Distortion - What It Is And How It's Measured*, Elliott
  Sound Products, October 2022.
  <https://sound-au.com/articles/distortion.htm>
- [S053] Bill Whitlock, *An Overview of Audio System Grounding & Interfacing*,
  presentation slides, 9/4/2012.
  <https://jhbrandt.net/assets/resource/An_Overview_of_Audio_SystemGrounding_and_Interfacing.pdf>
- [S055] Douglas Self, *Distortion In Power Amplifiers*, updated 12 September
  2019. <http://www.douglas-self.com/ampins/dipa/dipa.htm>
- [S057] Giuseppe Parolo, *Measurement of Complete Nonlinear Distortion in
  Audio Amplifiers via the Parallel Wiener-Hammerstein Model*, Journal of the
  Audio Engineering Society 74(5), 304-325, May 2026.
  <https://doi.org/10.17743/jaes.2022.0262>

## Unverified and open gaps

- IEC 60268-3 and AES17 are referenced by the practical sources but are not in
  the registry as full-text verified standards; the definitions here are from
  RaneNote 145 and should be checked against the standards before a compliance
  claim.
- Audio analyzer calibration, notch-filter design and FFT windowing/leakage:
  no verified procedural source yet.
- The full text of S057 is paywalled; only its abstract-level claim is used.
  The parallel Wiener-Hammerstein procedure itself is not reproduced here.
- Acoustic measurements (SPL, polar response, room response, distortion versus
  SPL): not covered by this document.
- Psychoacoustic audibility thresholds and listening-test statistics: not
  covered; see `psychoacoustics.md` when it exists.
- PSRR injection-fixture design and measurement uncertainty: not specified.
- True-peak measurement implementation details beyond the BS.1770 scope: not
  covered.
- Loudness measurement for object audio and advanced channel layouts: BS.1770-5
  extends beyond the five-channel example used here; open the standard for the
  full layout.

See `references/source-gaps.md` for the live list.
