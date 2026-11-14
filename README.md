# Flame in Freefall — Team Thu

A small Python/Streamlit dashboard for finding NASA combustion evidence. It has **Explore**, **Compare**, **Ask**, and **Sources & privacy** screens. The team reports that this release opens locally. Source repository: https://github.com/Iamsulav10/Flame-in-Freefall . No public demo URL or completed competition submission has been verified.

Ask includes a working evidence-based fallback. It ranks records and displays existing, cited statements. **It does not call a language model or generate new scientific claims.** No API key is needed. The source dataset contains 4 investigations, 30 traceable claims and 9 NASA sources; it contains no raw experiment files.

## Run on Windows

Install Python 3.12 from python.org. Extract this folder. Open **Terminal or PowerShell in this folder**, not the Python `>>>` prompt. Run one line at a time:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`. Stop the server with Ctrl+C. You do not need to activate the environment or change PowerShell execution policy.

## Run on macOS or Linux

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Start Streamlit from this folder so it reads `.streamlit/config.toml`.

## Try the demo

1. In **Ask**, leave the supplied smoke-detection question and click **Find evidence**.
2. Read the short evidence summary and its source buttons. SAME-R should rank first.
3. Expand **Inspect SAME-R**, inspect the findings and differing transport-time ranges, then open a NASA source.
4. In **Compare**, select SAME-R and Saffire-II. Notice different measurement types and “Not reported” entries.
5. Try an unrelated question, such as “Who won the football world cup?” It should report no matching evidence.

## Understand the files

| File | Responsibility |
|---|---|
| `app.py` | Draws screens and handles clicks |
| `evidence.py` | Checks records, ranks matches, selects cited statements |
| `data/evidence.json` | Stores sources, claims, conditions and study records |
| `.streamlit/config.toml` | Sets theme, disables optional telemetry, keeps security protections |
| `tests/` | Checks retrieval, comparison, errors and Streamlit interactions |
| `requirements.txt` | Exact tested runtime versions; only Streamlit is a direct dependency |
| `docs/` | Data dictionary, science explanation, privacy, deployment and submission draft |
| `reports/` | Actual validation outputs and remaining limitations |

## Test

```powershell
.venv\Scripts\python -m unittest discover -s tests -v
```

On macOS/Linux replace the Python path with `.venv/bin/python`. AppTest exercises Streamlit widgets but does not prove a phone layout or public browser access. See `reports/VALIDATION.md` for what was and was not checked.

## Deploy and submit

The team repository is https://github.com/Iamsulav10/Flame-in-Freefall . Use `docs/DEPLOYMENT.md` for Streamlit Community Cloud deployment; its older repository-access status is superseded by this link. Keep secrets out of Git and chat. The current app has no external AI configuration to enable. `docs/SUBMISSION_DRAFT.md` is reviewable text, not a submitted entry. Confirm the official challenge's complete resource list, Kathmandu requirements and current form limits before final submission.

The published global window is 14 November 2026 09:00 through 15 November 2026 23:59 local time. Build work began after 09:00 Nepal time. See `docs/RULES.md` for sources and unresolved details.

Code and original paraphrases: MIT. NASA and other upstream materials retain their own terms. See `LICENSE`, `docs/SOURCES.md`, `docs/THIRD_PARTY.md` and `docs/AI_ASSISTANCE.md`. Teammates still need to verify the source claims.

## Repository check — 14 November 2026

The uploaded application and data at commit `cefcde6673d9631b32ed661191e6f622d1ea40ee` matched the tested source release. This repair restores the missing requirements, configuration, README, license and ignore file. The team reports a local launch on Python 3.14.7; automated validation used Python 3.12.14. A local launch does not replace public desktop/mobile and source-link testing. Earlier documentation stating that no team repository exists is historical; deployment, current form requirements and final submission remain pending.
