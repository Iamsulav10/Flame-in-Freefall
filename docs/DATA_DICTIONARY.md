# Evidence structure and adding a study

`data/evidence.json` is a hand-curated, AI-assisted source index. It is not a NASA experiment-data download. Human verification is pending. All dates use ISO format; the build timestamp includes Nepal's UTC+05:45 offset.

| Field | Meaning |
|---|---|
| `schema_version` | Format version, currently 1 |
| `created_at`, `updated_on` | Creation timestamp and latest source-edit date |
| `raw_data_downloaded` | False for this release; do not change without a revised data workflow |
| `ai_assistance` | Machine-readable disclosure of assistance and review status |
| `sources` | Stable internal source IDs mapped to official URLs and metadata |
| Source `persistent_id` | DOI, NTRS ID or named persistent page; explicitly states when DOI is unverified |
| Source `access_level` | What was actually reviewed: indexed catalog, abstract, or summary; never implies raw data |
| Source `license`, `checked_on` | Verified rights statement or explicit uncertainty, and access date |
| `claims` | Stable IDs for individually traceable statements |
| Claim `text` | Short paraphrase, never a synthetic measurement |
| Claim `source_id`, `locator` | Official source and exact section/page supporting this statement |
| Claim `evidence_type` | `experiment_record`, `published_finding`, `hypothesis`, or `interpretation` |
| Claim `context` | Material, method, scope and qualifications needed to read the value correctly |
| Claim `quantity` | Null for nonnumeric text; otherwise operator, value or min/max, and original unit |
| Claim `review_status` | AI extraction versus actual human source verification |
| `studies` | Investigation title, ID, category, purpose, findings, fields and search keywords |
| Study `fields` | Claim IDs for sample, oxygen, airflow, pressure, geometry, sensors, measurements and transport time |
| Empty field list `[]` | Not reported in included sources; never a zero |
| Study `findings` | Published results; empty if only objectives were extracted |
| Study `categories`, `keywords` | Team/AI relevance judgments used for discovery, not NASA rankings |
| `discrepancies` | Conflicting claims that must remain visible and separate |

`published_finding` includes a published paper's reported methods and observations. Its context says which is which. A catalog objective or apparatus capability remains `experiment_record`. No hypothesis is currently included in the answer corpus. `gravity_limit` is an explicitly labeled interpretation supported by NASA's FM2 motivation.

Numbers keep their original units and qualifiers: “up to” describes a capability, “procedure range” describes a method, and “most averages” does not describe every particle. The app does not convert or chart these numbers as interchangeable measurements. Oxygen's concentration basis is not supplied where the reviewed catalog does not state it.

## Add another verified study

1. Read its official NASA record and any publication used. Save the exact URL, persistent identifier, version and access date. Record whether you read an abstract, full methods or actual raw files. Do not infer access from a file listing.
2. Add a source object. Use an approved NASA hostname. If a new official host is necessary, review it and change the allowlist deliberately; do not accept arbitrary URLs from visitors.
3. Write one short claim at a time. Add its section/page/table and test context. Distinguish objectives, methods, results, hypotheses and interpretation. Use null for unknown quantities and empty comparison lists for missing fields.
4. Add the study with a purpose claim, any published finding IDs, the eight comparison fields, and a short keyword list. Set categories based on the actual evidence and label them as team classifications.
5. Have the other teammate independently check each claim and update `review_status` with their review date. Preserve conflicts until the original methods resolve them.
6. Run the tests; add a meaningful retrieval example for the new study. Update the UI's collection count and submission description when the collection size changes.

No source PDFs, images or raw measurements are bundled. If adding actual experiment files later, add file names, checksums, run IDs, licenses and a reproducible extraction script. Revise the schema and validation rather than implying the present summaries are raw data.
