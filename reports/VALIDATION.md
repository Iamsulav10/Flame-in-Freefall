# Validation record — 14 November 2026

## Completed

| Check | Observed result |
|---|---|
| Build window | Initial clock 09:05:47 Nepal time, after the specified 09:00 opening. No challenge implementation existed at preparation completion. |
| Clean setup | Created a separate `application-env` and installed the exact 34-package runtime requirements successfully. Python 3.12.14, Streamlit 1.67.0. |
| Dependency consistency | `pip check`: no broken requirements. |
| Automated tests | **23 tests passed** in the clean app environment. Full output: `tests.txt`. |
| Ask demo | SAME-R is first, score 11, matching smoke/detection. Summary selects purpose plus smoke-size and detector-relevance claims, with source buttons to PSI-101 and the two smoke papers. |
| Explore | Detection filter shows SAME-R; conflicting filter/search returns no matches; material names are searchable. |
| Compare | All 12 ordered pairs run without Streamlit exceptions; missing data displays “Not reported”; method warnings remain visible. |
| Unsupported/weak questions | Unrelated questions abstain. A question with smoke terminology but an unsupported sleep/dreams claim also abstains. Scope warnings cover operational settings and partial gravity. |
| External AI unavailable | Default no-provider path works. Injected timeout and invalid claim IDs in the future-selector interface return local evidence. This is a simulated interface fault, not a live provider outage. No provider is implemented. |
| Input/rendering | 600-character limit, per-session rate controls, untrusted source URL rejection and plain-text user rendering tested. Prompt-like instructions do not execute tools or alter source data. |
| Science structure | Source IDs and locators validate; absent values are not zero; the two smoke transport-time ranges remain separate. |
| HTTP startup | A real subprocess serves `/` and `/_stcore/health` with HTTP 200. `http-check.json` records the probe. |
| Initial cookies | No Set-Cookie header observed on the initial local HTTP requests. Browser-session and host cookies were not measured. No “cookie-free” claim is made. |
| Security configuration | Telemetry false; public error details none; CORS true; XSRF true; SameSite lax. `config-check.json` records loaded values. |
| Dependency advisory audit | pip-audit 2.10.1 checked all **34 pinned runtime packages**, zero listed advisories, zero skipped packages. Full JSON included. Versions are pinned but wheel hashes are not pinned. |
| Secret scan | detect-secrets 1.5.0, network verification disabled: no findings in the working tree and the initial implementation commit. Full scan scope/commit IDs are in `secret-scan.json`; final release scan accompanies the package. |
| Code/configuration review | Reviewed local-only data flow, URL allowlist, text rendering, absence of model/network/command execution in application logic, error behavior and security settings. |

Two stricter question-coverage tests initially failed during development. They exposed an overly permissive partial match and a missing operational warning in the early abstention branch. The coverage threshold and warning order were corrected; the final 23-test run passed. No change was made to NASA measurements to make a test pass.

The subsequent release scan flagged the Git commit identifier stored in `reports/secret-scan.json` as a high-entropy hex string. It was checked against `git rev-list --all` and is a public commit hash, not a credential. It was retained and documented as a false positive rather than suppressed globally. `Team_Thu_Release_Secret_Scan.json` in the release package records all scanned commits, raw findings and the review. No confirmed secret was found.

## Source availability

All nine source identities and substantive claims were checked against NASA catalog/publication text during research, with access levels stored in the dataset. PSI-25 retains the indexed catalog evidence reviewed during preparation; its current direct page had no extractable text in web retrieval. No raw experiment files were downloaded.

The direct HTTP probe returned 200 for the three PSI records, Saffire factsheet and FM2 page. All four NTRS direct probes timed out. NTRS abstracts were separately available through web retrieval/indexed NASA text. A 200 response for a JavaScript catalog does not prove its record content rendered. Exact results: `link-check.json`.

The native browser showed `NET::ERR_CERT_AUTHORITY_INVALID` for the smoke-paper page. No security warning was bypassed. This environment failure is not evidence that the NASA link is broken for judges.

## Unfinished checks and exact reasons

- **Desktop/mobile visual journey:** The browser could not reach the executor's isolated local server (`ERR_CONNECTION_REFUSED`). A server launched and probed within one executor call worked. AppTest verifies widgets/state, not layout, phone wrapping, touch targets, contrast in the actual browser, or keyboard focus. Native wrapping columns and a high-contrast theme are implemented, but visual accessibility is not certified.
- **Full demo question → inspected result → opened NASA page:** Automated ranking, expander presence and source URLs pass. The last external-browser step was blocked by the certificate error above.
- **Public deployment and signed-out access:** No team GitHub repository or authorized compatible hosting account was available. No production URL exists, so public, signed-out, load and host cookie/retention checks could not run.
- **Live AI behavior:** No provider/key/model integration exists. No real external failure, retention or cost-budget behavior is claimed.
- **Competition form:** Team URL, authenticated Project tab, current guide and Kathmandu-specific requirements were not available. Exact demo duration and character limits remain unverified. No entry submitted.
- **Human science review:** Both teammates still need to verify claims and explain the app; no independent scientific validation or engineering certification occurred.

## Reproduce and finish

From the project folder, install `requirements.txt`, then run `python -m unittest discover -s tests -v`. AppTest may print a harmless missing-ScriptRunContext warning in bare mode. Test results and HTTP observations regenerate in `reports/`.

After deployment, use a signed-out desktop browser and a phone (or a 390-pixel viewport): Ask the demo question, inspect SAME-R and open its NASA source; filter Explore; compare all intended demo fields; try an unrelated question; check keyboard access, overflow and actual cookies. Record the live URL, date, viewport/device and observations here. If dependencies/code change, rerun relevant tests, audit and secret scan.

These are limited checks against known advisories and recognizable secret patterns. They do not establish zero vulnerabilities or protection against every future attack.
