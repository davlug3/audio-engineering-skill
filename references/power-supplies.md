# Power Supplies

This document covers the linear power supply behind an audio circuit: mains
input, transformer, rectifier, reservoir, regulator or capacitance multiplier,
and the supply's interaction with the signal path. It is deliberately
conservative about mains safety and about switch-mode supplies, because those
areas need standards and layout evidence that this registry does not yet hold.

Every numeric or behavioural statement carries a claim ID. Claims are in
`evidence/*.jsonl`; the source registry is `catalog/sources.json`.

## 0. Safety and scope

Mains voltage is lethal. Do not build a mains-connected supply from a web
article alone. Work to the electrical code and the safety standard that apply
where the equipment will be used, and have the mains section inspected by a
competent person.

Three safety facts frame the rest of this document:

- Leakage-current limits depend on the standard and the equipment class. A UL
  summary gives 0.5 mA for portable cord-and-plug appliances and 0.75 mA for
  fixed or stationary three-wire appliances, with up to 3.5 mA permitted for
  some information-technology equipment with EMI filters [C187]. Check the
  standard for the product class; Whitlock's 3.5/5 mA summary is not universal
  [C115].
- A Class A GFCI trips at 4 to 6 mA [C189]. An RCD is a different device with
  different trip thresholds, and a GFPE rated at 30 mA or more is for equipment
  protection, not personnel protection [C190]. ESP's "about 20 mA" applies to
  the RCDs it describes [C132], not to a Class A GFCI.
- Disconnecting the safety earth can leave a live chassis if a fault occurs,
  and may be illegal and create liability [C133].

The last point is not negotiable. A ground loop is a signal-integrity problem;
it is never a reason to remove the safety earth. See
`grounding-shielding.md`.

**Out of scope for this document:** switch-mode supply design, mains
creepage and clearance dimensions, transformer construction, lithium or
battery supplies, and regulatory approval. These are recorded as gaps at the
end.

## 1. Start from the load

The supply is defined by the load current profile, not by a schematic. A
Class-AB amplifier may draw only 20 to 100 mA at idle but many amps when
driven, and each supply lead sees half-wave current pulses in sympathy with the
programme; the sharp transitions generate magnetic fields [C172]. A Class-A
amplifier draws its maximum current continuously, which makes poor earthing
more apparent and makes the transformer's leakage flux a larger concern
[C173].

| Load type | Current profile | Transformer VA rule | Reservoir rule | Ripple-current rule |
|---|---|---|---|---|
| Class-AB | Low idle, high peaks, half-wave pulses | About equal to amplifier power [C068] | 4,700 uF per 100 W into 8 Ohm; 10,000 uF per 100 W into 4 Ohm [C069] | About 2x peak output current, e.g. 7 A for 100 W/8 Ohm [C071] |
| Class-A | Continuous maximum | 4 to 5x amplifier power, up to 10x [C068] | 4,700 uF per 10 W into 8 Ohm [C069] | About 5x load current [C071] |
| Class-D | High efficiency, but supply modulates | Approximately nominal power, with adequate regulation [C068] | Follow the module's recommendation; not covered by the linear rules | Not covered by the linear rules |

These are starting points, not a substitute for a load budget. Write down:

- DC rail voltage and tolerance;
- continuous and peak load current;
- allowable ripple at the load;
- allowable supply sag under a transient;
- thermal environment and heatsink;
- fault conditions: shorted output, reversed connection, mains surge,
  loss of regulation.

A capacitor-input supply is not linear: current flows from the transformer
only when the AC voltage exceeds the stored capacitor voltage, so the current
waveform is highly non-linear and can inject noise into nearby wiring,
including speaker cables [C169]. This is why layout and grounding are part of
the supply design, not an afterthought.

## 2. Transformer

### 2.1 VA is not watts

Transformer VA rating is not the same as watts: power factor is `W/VA`, and a
capacitor-input rectifier draws current in short peaks, so the VA rating must
exceed the DC power [C049]. In ESP's 25 V RMS, 0.75 Ohm, 1.44 A DC, 4,700 uF
example, the secondary RMS current was 2.71 A and the peak current 6.40 A,
giving a power factor of about 0.73 [C050]. A 100 VA transformer is not a
100 W DC supply.

### 2.2 Voltage is specified at full load

Transformer secondary voltage is specified at full rated current into a
resistive load. A 100 VA, 30 V transformer gives about 33.5 V RMS unloaded and
about 45 V DC after a bridge; its DC output can fall from 46 V to 38 V at full
load, a regulation worse than 17% [C170]. Mains voltage is nominally 230 V or
120 V with about +/-10% tolerance but is often worse, and the secondary tracks
it, so calculated DC voltages are approximate [C171]. Design for the high-line
and low-line cases, not for the nominal.

ESP's 60 VA, 0.75 Ohm, 4,700 uF example had about 16% regulation at 1.61 A DC,
compared with about 5% for the same transformer into a resistive load [C059].
The difference is the rectifier and capacitor's peak current, not a faulty
transformer.

### 2.3 Current ratios

The RMS secondary current is approximately 1.8 times the DC current for a
bridge rectifier, 1.2 times for a full-wave centre-tap, and 1.8 times for a
dual supply loaded in common mode [C051]. Half-wave rectification should not be
used above a few milliamps because the DC component can saturate a transformer,
especially a toroid, at about 20 mA [C052].

### 2.4 Transformer type

Toroidal transformers have much higher inter-winding capacitance than EI
transformers and couple more common-mode mains noise; an electrostatic shield
or side-by-side windings reduce it [C060]. Transformer flux density is highest
at no load, so mechanical noise is greatest at idle and low audio levels
[C061]. A toroid's lower leakage flux is an advantage, but it is not zero
[C173].

### 2.5 VA selection

ESP's minimum rules are approximately equal to amplifier power for Class-AB, 4
to 5 times (up to 10 times) for single-ended Class-A, and approximately nominal
power for Class-D with adequate regulation [C068]. ESP also notes that some
manufacturers suggest a VA rating of only 0.7 times the maximum amplifier
power; this works for most music but does not give a stiff supply, and the DC
voltage collapses as current rises [C180]. Start at the minimum rule and
increase the VA if the regulation or thermal test fails.

## 3. Rectifier and reservoir

### 3.1 Capacitance

Required reservoir capacitance is approximately

```text
C = (I_L / delta_V) * k * 1,000 uF
```

with `k = 6` for 120 Hz and `k = 7` for 100 Hz ripple [C053]. For 50 Hz mains
and full-wave rectification the ripple is 100 Hz; for 60 Hz mains it is 120 Hz.
The formula gives about 3,500 uF per amp for 2 V peak-to-peak ripple at 50 Hz
and about 3,000 uF per amp at 60 Hz; ESP recommends a minimum of 2,000 uF per
amp DC, which allows about 3 V peak-to-peak [C054].

Worked example: 1.44 A, 2 V peak-to-peak, 50 Hz:

```text
C = (1.44 / 2) * 7 * 1,000 = 5,040 uF
```

which matches ESP's example [C053]. A 4,700 uF capacitor gives slightly more
ripple; a 6,800 uF gives margin.

### 3.2 Ripple current and capacitor selection

Capacitor ripple-current rating must not be exceeded; two 4,700 uF capacitors
usually have a higher combined ripple rating and lower ESR than one 10,000 uF
capacitor [C057]. ESP recommends a reservoir ripple-current rating of about
twice the peak output current for Class-AB, for example 7 A for a 100 W/8 Ohm
amplifier, and five times the load current for Class-A [C071].

Doubling the reservoir capacitance halves ripple voltage for a given load
current but changes steady-state RMS and peak transformer current very little;
it does substantially increase inrush current [C055]. The claim that large
reservoir capacitance causes steady-state transformer overheating is a myth;
the increase is an inrush transient, not a steady-state current [C056]. A
larger transformer has lower winding resistance and better regulation, but it
places greater ripple-current stress on the reservoir capacitor [C058].

### 3.3 Rectifier ratings

ESP's guidance is a 35 A/400 V bridge for amplifiers of 50 W or more, with
current of at least 6 A per 100 W into 8 Ohm or 12 A per 100 W into 4 Ohm, and
voltage of at least 200 V for 100 W into 8 Ohm or 100 V for 100 W into 4 Ohm
[C070]. These are practical rules, not a substitute for the diode datasheet's
peak inverse voltage and surge-current ratings. Check the worst-case mains
high line [C171].

### 3.4 Ripple estimate

With the formula above, a 4,700 uF reservoir and a 1.5 A DC load at 100 Hz
gives

```text
delta_V = (1.5 * 7 * 1,000) / 4,700 = 2.23 V peak-to-peak
```

and a 2 A load gives 2.98 V peak-to-peak. These are derived from [C053]. They
are the raw-supply ripple before any regulator or capacitance multiplier. The
load's PSRR and the regulator's rejection determine whether that is acceptable.

## 4. Regulators

### 4.1 Conventional series regulator

A conventional emitter-follower regulator is stable with almost any output
capacitor and ESR, but typically needs about 3 V input-to-output differential
[C082]. Its dropout is high, but its stability is forgiving. Use it when the
raw supply has enough headroom and the load is not sensitive to the last few
hundred millivolts.

The LM317 is a representative adjustable part:

- reference voltage 1.25 V typical, output adjustable from 1.25 V to 37 V,
  current limit 1.5 A [C103];
- `VOUT = 1.25 V * (1 + R2/R1) + IADJ * R2`, and bypassing the adjustment pin
  improves ripple rejection [C174];
- minimum load current 3.5 mA typical and 10 mA maximum at a 40 V differential
  [C175];
- RMS output noise 0.003% of VOUT over 10 Hz to 10 kHz [C104];
- ripple rejection 57 dB typical without C_ADJ and 62 to 64 dB with
  C_ADJ = 10 uF for the legacy chip; the new chip is 65 dB without and 66 to
  80 dB with C_ADJ, at VOUT = 10 V and 120 Hz [C105];
- line regulation 0.01%/V typical and 0.04%/V maximum at 25 C; load regulation
  25 mV for VOUT up to 5 V or 0.1 to 0.5% of VOUT [C106];
- thermal regulation 0.04%/W typical for a 20 ms pulse [C107];
- legacy TO-220 (KCS) junction-to-ambient thermal resistance 23.5 C/W [C176].

At 15 V output the 0.003% noise is 450 uV RMS (derived from [C104]). That is
fine for a power amplifier but may be too high for a low-noise preamp; use a
lower-noise regulator, a capacitance multiplier, or a post-filter, and verify
the result. The LM317's high ripple rejection with C_ADJ [C105] is not the
same as low output noise [C104].

Thermal example: 5 W in a TO-220 with 23.5 C/W raises the junction 117.5 C
above ambient (derived from [C176]). Check the datasheet's maximum junction
temperature and derate; do not assume the package can dissipate 5 W at a high
ambient.

### 4.2 Low-dropout regulators

An LDO uses a PNP or P-channel pass device with the output taken from the
collector or drain, so it relies on feedback for low output impedance and is
not inherently stable [C079]. Its advantages are low dropout and low
quiescent current; its costs are stability sensitivity, higher output noise at
current, and poorer PSRR near dropout.

- Dropout voltage is the input-to-output differential at which regulation
  ceases; in dropout a PMOS pass element behaves as a resistor, so
  `Vdropout = Iout * Ron` [C096].
- The TPS76733 3.3 V LDO has 350 mV typical dropout at 1 A, so it begins to
  drop out at about 3.65 V input [C097].
- Quiescent current is the difference between input and output current and
  includes the reference, error amplifier and pass-device base or gate current
  [C098].
- LDO dropout can be 100 to 200 mV at low current, versus about 3 V for a
  conventional regulator [C083].
- Output noise is specified as RMS noise over 10 Hz to 100 kHz with a constant
  load and ripple-free input; most output noise comes from the internal
  reference [C099].
- LDO output noise increases with output current and is critical when powering
  ADCs and DACs, which have much lower supply rejection than op-amps [C085].
- The LM317 has 0.003% of VOUT output noise (75 uV at 2.5 V), while a TPS76425
  has a little over 60 uV at 10 mA [C084].
- Stability often depends on output-capacitor ESR; a very low-ESR 10 uF ceramic
  may oscillate, and the TPS76050 example needs at least 100 mOhm for stability
  [C080]. Adding more output capacitance can make an LDO less stable, not more
  [C081].
- Stability is specified as a range of compensation series resistance
  (`CSR = ESR + added resistance`) versus output current; the TPS763xx example
  is stable for CSR between 0.2 Ohm and 9 Ohm, the so-called tunnel of death
  [C100].
- High-K ceramic dielectrics lose capacitance with applied voltage, aging and
  temperature, which can affect stability [C086].
- Bypass capacitors on IC supply rails are part of the LDO output capacitance
  and can cause unforeseen stability problems [C087].

A larger output capacitor with low ESR improves PSRR, provided the CSR
stability requirement is met [C101]. That "provided" is the whole design: the
capacitor that gives the best ripple rejection may be outside the stable CSR
window.

#### LDO design procedure

1. Calculate the maximum load current and the minimum input voltage.
2. Check dropout at that current and temperature [C096][C097]. Leave margin
   for transient load steps and mains low line.
3. Calculate dissipation `(Vin - Vout) * Iout` and check the package thermal
   resistance. A 1.7 W example in a small package may need a heatsink.
4. Select an output capacitor that satisfies the CSR window at the actual
   ESR, including aging and voltage coefficient [C080][C086][C100].
5. Check that the IC bypass capacitors do not add unintended output
   capacitance [C087].
6. Check output noise at the actual load current [C085][C099].
7. Check PSRR at the ripple frequency and the actual load/headroom
   [C089][C090][C091].
8. Verify stability with a load-step test and a ripple-injection test; do not
   rely on a nominal "stable with ceramic" claim.

### 4.3 Capacitance multipliers

A capacitance multiplier is a buffered filter, not a literal capacitance
multiplier; a two-pole version changes the roll-off from 6 dB/octave to
12 dB/octave [C072]. The transistor buffers a high-impedance RC filter, so a
1 kOhm and 1,000 uF combination can be used at high current.

- A 1 kOhm and 1,000 uF filter has a 0.159 Hz corner and attenuates 100 Hz
  ripple by about 56 dB, reducing 1 V RMS to 1.6 mV [C073].
- Two 500 Ohm resistors and two 500 uF capacitors give nearly 74 dB at 100 Hz
  in ESP's second-order example; about 60 dB is achieved in practice [C074].
- A resistor from the output to ground keeps the output just below the ripple
  trough; without it the output ripple is more than 30 times greater [C075].
- A capacitance multiplier is intolerant of an output short circuit; the
  series-pass transistors can fail almost instantly, with no safe short-circuit
  duration [C076].
- In ESP's comparison the two-pole multiplier gave 246 mV peak-to-peak ripple
  versus just over 1 V for a pi filter, but dropped about 2.7 V at 3.6 A and
  dissipated about 10 W [C077].
- A MOSFET capacitance multiplier typically loses at least 4.5 V and has poor
  transient response because the gate has no rapid discharge path, with the
  gate staying high for up to 250 ms [C078].

Use a capacitance multiplier when the raw ripple is too high for the
regulator, or when a regulator's dropout is too high for the available
headroom. Do not use it as a short-circuit-protected supply. Add current
limiting or a fast fuse, and verify the worst-case dissipation.

## 5. PSRR and supply noise

PSRR measures how well a regulator rejects ripple from its input. TI's SLYT202
defines it as 20 log (input ripple / output ripple), so a larger positive number
is better [C088]; TI's SLVA079 uses the reciprocal, output ripple / input
ripple, which gives a negative number [C102]. State the convention. The
frequency range matters: 10 Hz to 10 MHz is common for LDOs [C088]. A single
PSRR number without a frequency is not a specification.

LDO PSRR has three frequency regions [C089]:

1. from DC to the bandgap-filter roll-off, dominated by open-loop gain and the
   bandgap's own rejection;
2. from there to the unity-gain frequency, dominated by open-loop gain;
3. above unity gain, where the output capacitor and parasitics dominate.

The design consequences:

- Higher load current lowers open-loop gain and therefore low-frequency PSRR,
  while moving the output pole higher and raising high-frequency PSRR [C090].
- When `VIN - VOUT` falls below about 1 V the pass FET can enter the triode
  region, reducing loop gain and PSRR; the required headroom rises with load
  current [C091].
- PSRR is usually better at lower output voltages [C092].
- A larger output capacitor with lower ESR typically improves PSRR above the
  unity-gain frequency, but can reduce it at some frequencies by lowering the
  unity-gain frequency [C093].
- The bandgap reference is a dominant internal PSRR path; it is usually
  filtered by a large internal resistor and an external capacitor [C094].
- Board layout must reduce input-to-output feedthrough parasitics to preserve
  LDO PSRR [C095].

Measure PSRR by injecting a known ripple into the input and measuring the
output at the same frequency, at the actual load and headroom. Do not compare
datasheet PSRR curves at a different load or a different input-output
differential. The LM317's 57 dB at 120 Hz without C_ADJ and 62 to 64 dB with
10 uF [C105] is a useful reference, but it is one part at one condition.

## 6. Fusing, inrush and protection

- Toroidal transformers need slow-blow fuses; a toroid of 500 VA or more
  benefits from soft start; a 100 W/8 Ohm amplifier may need a 3 A slow-blow
  fuse at 240 V or 6 A at 120 V [C062].
- A primary fuse does not protect the amplifier against output overload or
  shorted speaker leads; secondary DC fuses should always be used [C063].
- With transformers of 300 VA or less, inrush is typically limited by primary
  resistance and mains impedance to about 50 A at 230 V and lasts less than
  one AC cycle; larger transformers need soft start [C064].
- A soft start should limit peak current to 2 to 5 times the normal full-power
  operating current; for a 2 A maximum at 230 V this means 23 to 58 Ohm
  [C065].
- A switch-mode supply has no transformer primary resistance to limit inrush;
  ESP measured 80 A peak for a 150 W SMPS and more than 10 A for a 20 W SMPS
  [C066].
- A conventional linear supply is repairable and long-lived, while a
  switch-mode supply often fails through high-ESR electrolytic capacitors and
  may be unrepairable once specialised ICs are unavailable [C067].

The fuse is not a substitute for a safety earth. The safety earth must remain
connected [C133], and the mains wiring must be physically separated from the
signal and speaker wiring [C169].

## 7. Layout

The supply layout is part of the circuit:

- The ground point for a split supply must be taken from the centre tap of the
  filter capacitors, not from the transformer centre tap, and DC must be taken
  from the filter capacitors, not from the rectifier [C140].
- Capacitance-multiplier wiring should use a star topology, a ground area large
  enough for all connections but not so large that circulating currents flow,
  and the shortest possible capacitor leads [C141].
- An earth wire must not be routed so that it forms a partial or full turn
  around a transformer; relocate the star point or transformer if necessary
  [C138].
- A transformer core (EI or C-core) and any electrostatic shield must connect
  directly to chassis and safety earth, not through a loop breaker [C139].
- A 10 Ohm loop breaker reduces a 2 to 5 A shield current, caused by about 1 V
  RMS between separate earth connections, to less than 200 mA [C137].

The loop breaker is a signal-integrity and safety compromise, not a licence to
remove the safety earth. See `grounding-shielding.md` for the full treatment.

## 8. Worked supply example: 100 W into 8 Ohm, Class-AB

This is a sizing example, not a complete mains design. It uses ESP's rules for
a 100 W/8 Ohm Class-AB amplifier.

| Item | Value | Basis |
|---|---|---|
| Transformer | At least 100 VA; increase if regulation or thermal test fails | [C068] |
| Reservoir | 4,700 uF minimum | [C069] |
| Reservoir ripple rating | At least 7 A | [C071] |
| Rectifier | At least 6 A, 200 V | [C070] |
| Fuse | 3 A slow-blow at 240 V, or 6 A at 120 V | [C062] |
| Soft start | Not required at 100 VA; required at 500 VA or more | [C062] |

Check the ripple with [C053]:

```text
delta_V = (I_L * k * 1,000) / C
```

At 1.5 A and 100 Hz: `(1.5 * 7 * 1,000) / 4,700 = 2.23 V peak-to-peak`.
At 2 A: `2.98 V peak-to-peak`. The raw supply is therefore not low-noise; the
amplifier's PSRR and the wiring layout must handle it.

Check the secondary RMS current with [C051]: `1.8 * I_DC`. At 1.5 A DC that is
2.7 A RMS; at 35 V RMS that is about 95 VA, close to the 100 VA minimum. At
2 A DC it is 3.6 A RMS, about 126 VA, so a 100 VA transformer would be
overloaded. Size for the continuous current you actually specify, not for a
music-duty average.

Check the capacitor voltage rating against the maximum unloaded rail. A 100 VA,
30 V transformer gives about 45 V DC unloaded [C170], and mains high line can
push that higher [C171]. Use a capacitor rated above the worst-case unloaded
voltage, with the datasheet's derating.

Thermal design of the transformer, rectifier and reservoir is not covered by a
verified rule here. Measure the temperature rise at full load in the intended
enclosure and record the result.

## Sources

All sources below were opened on 2026-11-08. Claim locators are in
`evidence/*.jsonl`.

- [S042] Rod Elliott, *Linear Power Supply Design*, Elliott Sound Products,
  copyright 2001, updated May 2021.
  <https://sound-au.com/power-supplies.htm>
- [S043] Rod Elliott, *Capacitance Multiplier Power Supplies*, Elliott Sound
  Products, copyright May 2022, updated June 2026.
  <https://sound-au.com/articles/cap-multiplier.htm>
- [S044] Rod Elliott, *LDO Regulators: A Short Primer on These Sometimes
  Difficult Devices*, Elliott Sound Products, 2017.
  <https://sound-au.com/articles/ldo-regulators.htm>
- [S048] Rod Elliott, *Earthing (Grounding) Your Hi-Fi*, Elliott Sound
  Products, created 1999, updated December 2014.
  <https://sound-au.com/earthing.htm>
- [S050] John C. Teel, *Understanding power supply ripple rejection in linear
  regulators*, Texas Instruments Analog Applications Journal, 2Q 2005.
  <https://www.ti.com/lit/pdf/slyt202>
- [S051] Bang S. Lee, *Understanding the Terms and Definitions of LDO Voltage
  Regulators*, Texas Instruments application report SLVA079, 1999.
  <https://www.ti.com/lit/pdf/slva079>
- [S052] Texas Instruments, *LM317 3-Terminal Adjustable Regulator*,
  datasheet SLVS044Z, revised April 2025.
  <https://www.ti.com/lit/ds/symlink/lm317.pdf>
- [S053] Bill Whitlock, *An Overview of Audio System Grounding & Interfacing*,
  presentation slides, 9/4/2012.
  <https://jhbrandt.net/assets/resource/An_Overview_of_Audio_SystemGrounding_and_Interfacing.pdf>
- [S058] Underwriters Laboratories, *UL Question Corner: Leakage current*,
  IAEI Magazine, 18 February 2019.
  <https://iaeimagazine.org/columns/ul-question-corner/ul-question-corner-leakage-current/>
- [S059] Underwriters Laboratories, *Understanding Ground Fault and Leakage
  Current Protection*, The Code Authority: Electrical Connections newsletter,
  January 2009.
  <https://code-authorities.ul.com/wp-content/uploads/2014/04/ul_GroundFaultProtectiveDevices.pdf>

## Unverified and open gaps

- Switch-mode supply design for audio: no verified source in the registry yet.
- Mains creepage, clearance, insulation coordination and regulatory approval:
  no verified standard in the registry; the UL leakage and GFCI summaries are
  not the standard text [C187][C189]. Use the applicable standard and a
  competent inspector.
- Transformer thermal design and hotspot measurement: no verified rule.
- Reservoir capacitor lifetime, ESR versus temperature and ripple-current
  derating beyond the basic rating: no verified rule.
- Bleeder resistor sizing and discharge time: no verified rule.
- Soft-start component selection (NTC, relay, resistor) and its interaction
  with fusing: only the current-limit ratio is evidenced [C065].
- LDO output-capacitor selection beyond the CSR window, and the effect of
  capacitor aging: the stability requirement is evidenced [C100], but the
  end-of-life calculation is not.
- Regulator loop compensation and stability across load: simulate in
  `circuit-design-skill`; the datasheet is the authority.
- PSRR measurement uncertainty and injection-network design: see
  `measurement.md`; the fixture is not yet specified.
- Battery and portable supplies: out of scope.

See `references/source-gaps.md` for the live list.
