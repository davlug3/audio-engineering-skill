# Research Protocol

The rule is simple: **do not answer an audio-circuitry question from memory.**
Recall may propose a hypothesis or a search query. It may not supply a value,
part, pinout, topology, limit or standard.

## 1. Triggers

Research is mandatory for:

- component values, tolerances, ratings and derating;
- device behaviour, bias points and operating limits;
- topology selection and circuit blocks;
- part numbers, packages, pinouts and second sources;
- distortion, noise, bandwidth, slew rate and headroom claims;
- power, thermal, safety and protection;
- standards, loudness, weighting and measurement methods;
- acoustic and perceptual claims;
- any statement of the form "this sounds better", "this is standard",
  "this is safe" or "this is a known issue".

## 2. Search order

Prefer primary and high-provenance sources:

1. Manufacturer datasheet and application note for the exact part and revision.
2. Standards body document (ITU, IEC, ISO, AES) for measurement and limits.
3. Peer-reviewed paper (JAES, JASA, IEEE, Applied Acoustics, JSV) for methods
   and perceptual results.
4. Textbook or monograph with edition and ISBN for established theory.
5. Named-author practitioner article or manufacturer design note for practical
   implementation detail.

Use Crossref, OpenAlex, Semantic Scholar, DOAJ and arXiv to *find* papers.
Cite the paper, not the index.

## 3. Query construction

- Include the part number, revision and parameter name.
- Include the measurement condition: level, frequency, load, bandwidth.
- Prefer exact document titles and standard numbers.
- Search for the failure mode explicitly ("oscillation", "thermal runaway",
  "ground loop", "input bias current noise").
- Search for a contradicting source on purpose before finalising a rule.

## 4. Open the source

Search snippets, AI summaries and aggregator pages are leads, not evidence.

- Open the document and confirm the claim in context.
- Record the locator: section, page, clause, table or figure.
- Record the access date and the URL or DOI actually opened.
- If the document is paywalled, cite the metadata and abstract; do not claim to
  have read the full text.
- If a page has changed or disappeared, record it as `broken` or `superseded`
  and do not rely on a remembered copy.

## 5. Evidence extraction

Write the claim to `evidence/<topic>.jsonl` before writing prose:

```json
{"id": "C001", "statement": "The device is specified for a 10 kOhm load",
 "value": 10000, "unit": "ohm", "conditions": "Vs = +/-15 V, 1 kHz",
 "source": "S004", "locator": "datasheet p. 5, table 2",
 "confidence": "high", "checked": "2026-11-08"}
```

Prose cites `[C001]`. A claim without a source id is a hypothesis.

## 6. Evidence thresholds

| Claim type | Minimum |
|---|---|
| Part parameter | one primary source (datasheet, exact revision) |
| Design rule or limit | two independent sources |
| Perceptual or audibility claim | two independent peer-reviewed sources |
| Safety or regulatory | the governing standard, quoted by clause |
| Conflicting sources | three sources, and the conflict stated explicitly |

Where the only available evidence is Tier 3, two independent Tier 3 sources are
acceptable for an implementation rule, provided the prose labels it
**practitioner guidance** and the gap is recorded in
`references/source-gaps.md`. This exception does not apply to safety,
regulatory or perceptual claims. Do not average conflicting values into a
made-up consensus.

## 7. Recency and revision

- Check the datasheet revision and the standard edition before citing.
- Prefer the current revision of a standard; record what changed if an older
  revision is still in use.
- Note obsolete or last-time-buy parts.

## 8. When the web is unavailable

Say so plainly. Produce:

- the question list,
- the search terms and sources to try,
- what is already verified,
- what remains unverified.

Never fill the gap from memory. An answer without sources is a plan, not a
result.

## 9. Required answer format

Every substantive audio answer ends with:

```
## Sources
- [S004] Title, author/publisher, revision, locator, URL, accessed YYYY-MM-DD.

## Unverified
- Hypotheses or gaps not traced to a source, and the test that would settle them.
```

If there is nothing to list under Sources, the answer is not finished.

## 10. Anti-patterns

- "It is well known that..." with no source.
- Citing a search result, a forum post or an AI summary.
- Quoting a THD number without level, frequency, bandwidth and load.
- Treating a vendor's marketing graph as a guaranteed limit.
- Presenting a simulation as a measurement.
- Hiding a gap instead of recording it.
- Using a source from memory, then back-filling a plausible URL.
