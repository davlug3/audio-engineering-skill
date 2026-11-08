# Grounding and Shielding

Grounding is two problems with one name. The first is **safety**: the chassis
must be connected to protective earth so that a fault trips the breaker instead
of electrifying the case. The second is **signal integrity**: the audio return,
the shield and the chassis must be arranged so that noise currents do not flow
through the signal reference. A design that solves the second by weakening the
first is not a design.

Every numeric or behavioural statement carries a claim ID. Claims are in
`evidence/*.jsonl`.

## 0. Safety first

- Leakage-current limits are not one universal number. A UL summary gives
  0.5 mA for portable cord-and-plug appliances and 0.75 mA for fixed or
  stationary three-wire appliances, with up to 3.5 mA permitted for some
  information-technology equipment with EMI filters [C187]. Whitlock's 3.5/5 mA
  figures come from a different summary and must be checked against the
  standard for the product class [C115].
- A Class A GFCI trips at 4 to 6 mA [C189]. A 30 mA European RCD is a different
  device, and a GFPE that trips at 30 mA or more is for equipment protection,
  not personnel protection [C190]. ESP's "about 20 mA" is a practitioner
  summary of the RCDs it describes [C132]; do not apply it to a Class A GFCI.
- Safety grounding must never be defeated to solve a noise problem; doing so is
  dangerous, illegal in many jurisdictions, and creates liability [C126].
- NEC 2008 Articles 250.6(D) and 250.114 prohibit removing safety grounding
  from plug-and-cord-connected equipment to solve noise issues; signal cables
  are not safety-ground wiring [C127].
- Disconnecting the safety earth can leave a live chassis if a fault occurs,
  and may be illegal and create liability [C133].
- A ground-lift feature is legally allowed to interrupt safety ground only when
  the unit provides a GFCI on its output; a premises GFCI outlet must still
  have its safety ground connected if one is available [C131].

The correct order is: make the safety earth robust, then break the signal loop
in the signal path [C128]. If the only way to remove hum is to lift the safety
earth, the design has a grounding defect, not a grounding solution.

## 1. What a ground loop is

A ground loop is formed when two units' signal grounds are tied together in
more than one place, for example by the signal cable and by the safety earth;
hum occurs when the resulting current flows through a unit's audio signal
ground [C108]. The voltage that drives the current appears between the
independent grounds of the units, and the loop impedance is low, so the current
can be large even when the voltage is small [C108].

Common-mode voltage has three main sources [C119]:

1. a voltage difference between driver and receiver grounds;
2. magnetic-field induction in the cable;
3. electric-field induction in the cable.

The first is the one that the safety-earth topology controls. The second is
why cable routing and transformer placement matter. The third is why shields
and chassis bonding matter.

AES Convention Paper 8234 shows that the second source, magnetic induction in
premises AC wiring, can dominate. In one installation, 30 A rms per phase
produced about 650 mV rms between cable shield pins; twisting the
current-carrying conductors reduced it to less than 3 mV rms [C183]. Twisting
line and neutral at about five twists per foot gave the lowest induced voltage
of the tested configurations, and the worst case was over 1,000 times worse
[C184]. The authors conclude that leakage currents cannot account for the much
higher ground voltages seen in the field [C185]. This is why measuring the
shield voltage and current, and inspecting the premises wiring, is part of the
audio grounding job.

A useful diagnostic is to measure the voltage between the chassis of the two
units, then measure the current in the shield. If the shield current changes
when a source is connected or disconnected, the loop is in the interconnect.
If it changes when the mains plug is reversed or a different outlet is used,
the loop is in the mains safety ground. Do not use a ground lift to test;
use a current clamp or a differential probe.

## 2. The balanced interface

### 2.1 It is about impedance, not equal-and-opposite signal

A balanced interface rejects noise through common-mode impedance balance, not
through equal-and-opposite signal voltages; this is the definition in
IEC 60268-3 [C117]. A balanced circuit is a two-conductor circuit in which both
conductors and all connected circuits have the same impedance with respect to
ground and to other conductors, so noise pickup is common-mode and can cancel
in the load [C118]. The signal can be on one line, unequal on both, or equal on
both; symmetry of the desired signal affects headroom and crosstalk, not noise
rejection [C117].

This matters because a design that only inverts the signal on the cold leg,
without matching the common-mode impedances, is not a balanced interface. It
may have a differential output, but it will not reject ground noise.

### 2.2 CMRR

CMRR is the ratio of differential-mode signal gain to common-mode noise gain,
is expressed in dB, and is not a signal level, so it must not be written as
dBu, dBV or dBm [C120]. A balanced interface behaves as a Wheatstone bridge;
rejecting ground noise requires a precise ratio match of the positive and
negative common-mode divider arms [C121].

Real-world common-mode impedances are imbalanced by about +/-10 Ohm at 60 Hz,
and the CMRR of the SSM-2141 receiver drops by 25 dB with only 1 Ohm of driver
imbalance [C122]. This is the single most important number in balanced
interface design: a receiver's advertised CMRR is not the interface CMRR you
will get with a real driver. The interface CMRR is limited by the source
impedance match, the cable, and the receiver's common-mode impedance.

With +4 dBu (1.23 V) reference level, 80 dB of interface CMRR and 15 dB of
headroom give 95 dB of total dynamic range, comparable to a CD; 50 dB CMRR is
rarely enough for a commercial system [C123]. Design for at least 80 dB of
real-world CMRR, and measure it with the actual driver and cable, not with a
laboratory source.

### 2.3 Shield termination

AES48 specifies balanced lines with the cable shield tied to the metal chassis
at both ends; a balanced line has two signal conductors plus a shield [C109].
XLR pin 1 should be tied to the chassis at the point of entry, not to the audio
signal ground [C110]. This is the "pin 1" rule, and it is the basis of the
shield's RF performance.

If a shield must be lifted, disconnect it at the receiving end and capacitively
couple it to the chassis with 0.1 uF or 0.01 uF; this is the hybrid shield
termination [C112]. The capacitor blocks the low-frequency ground current while
providing an RF return. The sending end remains bonded to the chassis.

Transformer isolation is the most reliable way to break a ground loop between
balanced and unbalanced equipment [C111]. It is also the most expensive and
the bulkiest; use it where the loop cannot be broken otherwise.

## 3. The pin 1 problem

The pin 1 problem is common-impedance coupling inside equipment that turns the
shield connection into a low-impedance signal input, allowing shield current to
flow in signal-reference conductors; Neil Muncy named it in 1994 [C124]. Good
designs give shield current a separate, direct route back to safety ground
instead of sharing signal-reference conductors [C125].

Symptoms:

- hum or buzz that changes when a cable is moved or a unit is touched;
- noise that appears only when a particular source is connected;
- noise that is unaffected by a ground lift on the signal cable but changes
  when the chassis bonding changes;
- RF interference that enters through the cable shield.

Fixes:

- bond the connector shell to the chassis at the entry point [C110];
- route the shield current to chassis on a dedicated conductor, not through the
  signal return [C125];
- keep the signal reference and the shield return separate on the PCB;
- use a hybrid termination if the shield must be lifted at one end [C112];
- do not use the signal cable's shield as a safety-ground conductor [C127].

Test the fix by injecting a known current into the shield and measuring the
output. A design that is quiet with the source disconnected but noisy with it
connected has a pin 1 or ground-loop problem, not a source problem.

## 4. Unbalanced interfaces

Any unbalanced cable should be kept under ten feet (three meters); longer
cables amplify the side effects of unbalanced ground loops [C113]. For
unbalanced interfaces, keep cables short, use heavy shields, avoid unnecessary
grounds, never disconnect safety ground, use isolators at problem interfaces,
and separate signal and power bundles by at least 6 inches [C129].

An unbalanced interface is inherently more susceptible because the shield is
part of the signal return. The practical rules are:

- use the shortest cable that reaches;
- use a heavy braided shield, not a foil-only shield;
- do not coil excess cable near a transformer or motor;
- do not add a second ground at the destination;
- use a transformer or an active isolator for long runs [C111];
- keep the safety earth connected [C126].

## 5. Chassis, star and mesh

Mesh grounding approximates a ground plane at high frequencies and tolerates
loops; star grounding avoids shared conductors and is preferred for audio
because 60 Hz is in band [C130]. The two are not mutually exclusive. A good
audio chassis is a mesh at RF (multiple bonds, short wide connections) and a
star at audio (separate returns joined at one point).

Practical rules:

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

### 5.1 The loop breaker

A 10 Ohm loop breaker reduces a 2 to 5 A shield current, caused by about 1 V
RMS between separate earth connections, to less than 200 mA [C137]. The loop
breaker works by adding resistance in the earth return, with a parallel
capacitor for radio-frequency continuity and a diode bridge for fault current
[C179]. It is effective, but it may not be legal where you live [C177], and it
requires all input and output connectors to be insulated from the chassis;
otherwise the connector shell defeats it [C178].

The loop breaker is not a ground lift. The safety earth remains connected
through the resistor and the bridge; the resistor only reduces the low-level
circulating current. If the loop breaker is not legal in your jurisdiction, use
balanced interconnects or signal isolation instead [C177][C128].

### 5.2 Ground-lift switches

Ground-lift switches are band-aids: in most cases they do not improve ground
noise and they reduce the unit's ability to be properly grounded [C114]. A
ground-lift feature that actually disconnects the safety earth is only legal
with a GFCI on the output [C131]. Do not ship a product that relies on a
ground-lift switch for normal operation.

## 6. Cabling and shielding

- Use twisted-pair balanced cable with a shield bonded to the chassis at both
  ends [C109].
- For a shield lift, use the hybrid termination at the receiving end [C112].
- Keep unbalanced cables under three meters [C113].
- Separate signal and power bundles by at least 6 inches [C129].
- Put RF capacitors at the input connector, returned to the connector shield,
  plus a third capacitor to shunt differential RF inside the enclosure [C042].
- Do not route an earth wire in a partial turn around a transformer [C138].
- Keep DC, speaker and signal wiring away from the transformer; transformer
  leakage flux can cause buzz [C173].

The shield is not a drain for signal current. It is a return for interference
current, and it must reach the chassis without sharing the signal-reference
path [C125].

## 7. Design procedure

1. **Safety.** Bond the chassis to protective earth with a dedicated,
   approved connection. Fuse the mains. Verify leakage current against the
   limit for the product class [C187], not against a single remembered number.
   Do not rely on the RCD or GFCI as the only protection [C132][C189].
2. **Draw the topology.** Mark chassis, safety earth, signal reference, PSU
   return, shield, and every cable shield. Identify every loop.
3. **Break loops in the signal path.** Use balanced interfaces [C109],
   transformer isolation [C111], or a hybrid shield termination [C112]. Never
   break the safety earth [C126].
4. **Fix pin 1.** Bond connector shells to the chassis at the entry point
   [C110]; route shield current separately [C125].
5. **Star the audio returns.** Join signal returns at one point; keep the PSU
   return at the capacitor centre tap [C140]; keep noisy returns separate
   [C130].
6. **Mesh the chassis at RF.** Multiple short bonds; keep the shield
   continuous; use the chassis as the RF reference.
7. **Test.** Measure hum and noise with the source connected and disconnected;
   inject shield current; sweep CMRR from 20 Hz to 20 kHz with the real driver;
   check the RCD; run a fault-current test if qualified.
8. **Document.** Record the ground topology, the measured shield current, the
   CMRR at 60 Hz and 1 kHz, and any deviation from this document.

## 8. The ESP/Whitlock contradiction

ESP argues that ground loops are not caused by leakage current because a
leakage path from the active line would trip the safety switch instantly
[C135]. Whitlock documents leakage current from parasitic capacitances,
including transformer winding-to-winding capacitance and internal EMI filters,
as a real 60 Hz current [C116], and quotes leakage limits in the 0.75 to
5 mA range [C115]; UL's own summary gives the product-class-dependent values
in §0 [C187].

Both statements can be true:

- A **fault** from the active line to chassis is a high current; it trips the
  overcurrent device, and a ground fault above the trip threshold also trips a
  GFCI or RCD [C189][C190].
- **Capacitive leakage** in normal equipment is limited to the product-class
  values in §0, typically 0.5 to 0.75 mA for cord-and-plug appliances and up
  to 3.5 mA for some information-technology equipment with EMI filters [C187].
  That is below the 4 to 6 mA Class A GFCI trip [C189] and below the 30 mA
  RCD/GFPE threshold [C190], so it can flow continuously in the shield without
  tripping anything.
- Ground loops also have non-leakage sources: ground potential differences,
  magnetic induction and electric induction [C119].

A third mechanism often dominates: magnetic induction in premises AC wiring
[C182]. In the AES field case, 30 A rms per phase produced about 650 mV rms
between shield pins, and twisting the current-carrying conductors reduced it to
less than 3 mV rms [C183]. The authors state that leakage currents cannot
account for the much higher ground voltages observed in the field [C185]. So
the practical question is not whether leakage exists, but which mechanism
dominates in this installation: leakage, premises-wiring induction, or
magnetic/electric induction in the signal cable [C119].

ESP's argument is correct for a fault-level leakage path; it does not cover
sub-threshold capacitive leakage or premises-wiring induction. The practical
conclusion is to design for all three: keep the safety earth, limit leakage
with a proper transformer and EMI filter, twist and route premises wiring to
reduce magnetic induction [C184], measure the shield current, and use a signal
isolator or a hybrid termination where the loop cannot be broken otherwise
[C128].

The ESP claim is recorded with `confidence: low` and a note pointing to this
reconciliation. It is not used as a design rule.

## Sources

All sources below were opened on 2026-11-08. Claim locators are in
`evidence/*.jsonl`.

- [S040] Rane Technical Staff, *RaneNote 110: Sound System Interconnection*,
  written 1985, revised 11/15.
  <https://www.ranecommercial.com/legacy/note110.html>
- [S042] Rod Elliott, *Linear Power Supply Design*, Elliott Sound Products,
  copyright 2001, updated May 2021.
  <https://sound-au.com/power-supplies.htm>
- [S043] Rod Elliott, *Capacitance Multiplier Power Supplies*, Elliott Sound
  Products, copyright May 2022, updated June 2026.
  <https://sound-au.com/articles/cap-multiplier.htm>
- [S048] Rod Elliott, *Earthing (Grounding) Your Hi-Fi*, Elliott Sound
  Products, created 1999, updated December 2014.
  <https://sound-au.com/earthing.htm>
- [S053] Bill Whitlock, *An Overview of Audio System Grounding & Interfacing*,
  presentation slides, 9/4/2012.
  <https://jhbrandt.net/assets/resource/An_Overview_of_Audio_SystemGrounding_and_Interfacing.pdf>
- [S054] THAT Corporation, *Input and Output Circuits for THAT Preamplifier
  ICs*, Design Note 140, Doc 600140 Rev 03, 2011-2014.
  <https://thatcorp.com/datashts/dn140.pdf>
- [S056] Bill Whitlock and Jamie Fox, *Ground Loops: The Rest of the Story*,
  AES Convention 129, Paper 8234, 4-7 November 2010. Author-hosted copy:
  <https://jhbrandt.net/assets/resource/AES-Ground-Loops-Rest-of-Story-Whitlock-Fox.pdf>
- [S058] Underwriters Laboratories, *UL Question Corner: Leakage current*,
  IAEI Magazine, 18 February 2019.
  <https://iaeimagazine.org/columns/ul-question-corner/ul-question-corner-leakage-current/>
- [S059] Underwriters Laboratories, *Understanding Ground Fault and Leakage
  Current Protection*, The Code Authority: Electrical Connections newsletter,
  January 2009.
  <https://code-authorities.ul.com/wp-content/uploads/2014/04/ul_GroundFaultProtectiveDevices.pdf>

## Unverified and open gaps

- Shield transfer impedance and shielding-effectiveness numbers for specific
  cables: no verified source in the registry yet.
- RF immunity standards and test levels (IEC 61000-4-3 and related): no
  verified standard in the registry.
- Safety standard details for creepage, clearance and insulation coordination:
  use the applicable standard and a competent inspector.
- Mains filter design and leakage-current contribution of specific EMI
  filters: only the general mechanism is evidenced [C116].
- Isolation-transformer selection, inter-winding capacitance and shield
  construction: no verified selection rule.
- Turntable, tonearm and cartridge grounding: no verified source yet.
- PCB stackup and return-path design at RF: no verified source yet.
- CMRR measurement uncertainty and fixture design: see `measurement.md`; the
  fixture is not yet specified.
- The exact leakage current of a given product: measure it; the UL limits
  depend on the product class and are not a prediction [C187].

See `references/source-gaps.md` for the live list.
