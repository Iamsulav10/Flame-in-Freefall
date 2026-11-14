# Explain the project simply

**What problem do we solve?** NASA fire research is spread across experiment catalogs and papers. We help a reader find a relevant study and see the evidence behind a statement.

**How does the code work?** `evidence.json` is our set of labeled evidence cards. `evidence.py` checks those cards, matches words and synonyms, then selects existing statements. `app.py` displays them. A source button beside a statement lets the reader check it.

**Is Ask a language model?** No. This version is a deterministic evidence summary. Four points are awarded for each curated topic match, two for each additional evidence-text match, plus up to three points for related terms. Identical inputs return the same ranking. The score is not a probability or safety rating. AI helped build the project, but the running app makes no model calls.

**Why SAME-R for smoke detection?** Its catalog focuses on smoke particle sizes and transport. The reflight papers describe smoke diagnostics, including detector-related measurements. Read the source buttons; this does not mean SAME-R certified a commercial detector. Sources: PSI-101 Objectives and NTRS 20130000422 Abstract, linked in `SOURCES.md`.

**When does Ask decline to answer?** After removing common words, fewer than 60% of the question's distinct terms matching our topics/evidence produces a weak-evidence message. Between 60% and 75% produces a partial-match notice. These conservative word-coverage rules are heuristics, not a scientifically validated confidence model. Operational-setting and Moon/Mars questions also receive an explicit scope warning.

**Why no comparison chart?** These records describe different methods. Smoke particle size, solid flame spread and droplet extinction are not one measurement. Putting them on a common outcome chart would mislead the reader. We compare reported conditions with units and preserve missing values instead.

**Why do transport times differ?** NTRS 20130000422 says 11–1800 s; NTRS 20140006579 says 11–800 s. We have not reconciled their full methods. The app keeps each range beside its own source instead of choosing or averaging them.

**Can it predict fires on Mars?** No. Microgravity changes buoyancy; partial gravity on the Moon or Mars is another condition. NASA's FM2 page motivates dedicated partial-gravity work. Our app discovers evidence, not certified operating limits.

**What did we actually analyze?** Catalog descriptions, published abstracts and a factsheet. We did not analyze raw flight data or train a scientific prediction model.

**What is still limited?** Four studies, a small synonym list, no external AI service, no public deployment yet, and teammate verification still pending. The available browser could not complete visual desktop/mobile tests. This is a first working research tool, not an operational safety system.

## Two-person handoff

One teammate walks through Ask and checks each source. The other explains Compare and demonstrates missing data. Swap roles once. Both should be able to show where a claim comes from and explain the limits above. Before submission, review every claim together and update the AI-assistance log accurately.
