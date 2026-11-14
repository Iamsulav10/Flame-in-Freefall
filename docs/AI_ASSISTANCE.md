# AI assistance disclosure and work log

OpenAI ChatGPT/Codex substantially authored this prototype's code, paraphrased evidence records, tests and documentation in response to Team Thu's instructions. Team members set the goal and constraints. Human teammate verification is pending; do not describe the implementation as human-only or fully human-reviewed.

| Nepal date/time | Assistance actually performed | Human review |
|---|---|---|
| 14 November 2026, before 09:00 | Official-source research, preparation notes and a general Python environment; no challenge app or structured competition dataset | Pending |
| 14 November 2026, after observed 09:05 opening check; resumed in afternoon | Created `app.py`, `evidence.py`, dataset, configuration, tests, setup/deployment documentation and submission draft; checked official NASA sources and ran recorded validation | Pending |

The record distinguishes **development assistance** from **runtime behavior**. The running application uses deterministic word/synonym matching and prewritten evidence statements. It does not call an AI service, generate novel answers, train a model, analyze raw NASA files or create synthetic measurements.

AI selected relevant source passages and paraphrased them. Each data claim carries an evidence type, source ID, locator, context and review status. Study categories and retrieval keywords are team/AI interpretations. The JSON top-level `ai_assistance` field provides machine-readable disclosure. No AI images, audio or video were generated for this package.

Validation was executed by the assistant through Python tests, Streamlit AppTest, local HTTP checks, dependency auditing and secret scans; actual results and blocked browser checks belong in `reports/VALIDATION.md`. Do not infer human testing from automated test results.

Before submission, both teammates should inspect every scientific claim, run the app, explain the three workflows to one another, and update this log with what they personally reviewed. Add any later tools or provider calls accurately. Preserve this disclosure in the repository and the submission form.
