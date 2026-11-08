# Source Policy

The registry is the evidence backbone. A source is reliable because of its
provenance, method and traceability — not because it is popular.

## 1. Tiers

### Tier 1 — Standards and peer review

- Standards bodies: ITU, IEC, ISO, AES Standards.
- Peer-reviewed journals: Journal of the Audio Engineering Society (JAES),
  Journal of the Acoustical Society of America (JASA) and JASA Express Letters,
  IEEE journals, Applied Acoustics, Journal of Sound and Vibration.
- Official regulatory or metrology publications.

Tier 1 is required for limits, measurement methods, loudness and safety.

### Tier 2 — Books and monographs

Textbooks and specialist monographs with a named author, edition, publisher and
ISBN. Examples of the class: small-signal audio design, audio power amplifier
design, valve amplifiers, sound reproduction, acoustics, psychoacoustics,
switch-mode power supplies.

Tier 2 supports established theory and design method. Record the edition and
the page or chapter.

### Tier 3 — Practitioner engineering

- Manufacturer datasheets and application notes for the exact part revision.
- Manufacturer design notes from audio semiconductor and transformer vendors.
- Named-author technical articles with schematics, measurements and an
  identifiable author and date.
- Audio measurement instrument application notes.

Tier 3 is valid for implementation detail and part behaviour. A design rule or
limit taken from Tier 3 must be corroborated by Tier 1 or Tier 2.

### Not citable

Forums, wikis, anonymous or undated pages, content farms, marketing claims
without data, and AI-generated text. They may be used as leads only.

## 2. Access and licensing

- Link and cite paywalled papers; never mirror the PDF.
- Do not reproduce figures, artwork, PCB layouts or proprietary models.
- Record `access` as `open`, `paywalled` or `book`.
- Prefer an open-access version only when it is the same work; cite the
  published version and note the repository copy.
- Respect vendor terms for datasheets and models.

## 3. Registry schema

`catalog/sources.json`:

```json
{
  "schema_version": 1,
  "updated": "2026-11-08",
  "sources": [
    {
      "id": "S001",
      "tier": 1,
      "title": "Recommendation ITU-R BS.1770-5",
      "authors": ["International Telecommunication Union"],
      "year": 2023,
      "venue": "ITU-R",
      "doi": null,
      "url": "https://www.itu.int/rec/R-REC-BS.1770",
      "accessed": "2026-11-08",
      "status": "verified",
      "access": "open",
      "topics": ["loudness", "true-peak", "measurement"],
      "note": "In force edition; check for a newer revision before citing."
    }
  ]
}
```

Required fields: `id`, `tier`, `title`, `authors`, `year`, `venue`, `url` or
`doi`, `accessed`, `status`, `access`, `topics`.

Status values:

- `verified` — opened during a research session; may be cited.
- `candidate` — known lead, not yet opened; may not be cited.
- `broken` — URL or DOI no longer resolves; replace or archive.
- `superseded` — newer edition or document exists; keep for history, do not cite
  as current.

## 4. Coverage

- At least three independent sources per major topic.
- At least one Tier 1 source per major topic where one exists.
- Every target in `catalog/targets.json` cites at least one verified source.
- Every reference document has a `## Sources` section and resolvable citations.
- Missing coverage is recorded in `references/source-gaps.md`; do not fill it
  with prose.

## 5. Verification and maintenance

Quarterly, and before a release:

- resolve every URL and DOI;
- check for a newer datasheet revision or standard edition;
- mark dead links `broken` and superseded documents `superseded`;
- snapshot fragile pages with a web archive and record the snapshot URL;
- re-open any source that supports a safety or regulatory claim.

External reachability is an opt-in CI job so a vendor outage cannot fail the
normal test suite.

## 6. Citation format

In prose:

```
[Strapped supply noise is rejected by the regulator's PSRR [C014].]
```

`[C###]` refers to an evidence record; `[S###]` may be used for a direct
source reference where no claim record is needed. Both must resolve.
