# Team Thu — reviewable submission draft

**Status: built locally; not deployed or submitted.** The authenticated Project tab and current guide were not available. The field categories below follow the organizing-team answer at https://github.com/nasa/spaceapps/discussions/1858 (9 November 2026, points 3–5). Exact labels, character limits and mandatory fields remain unverified. Do not submit with missing links or before checking challenge-resource eligibility.

Go to **spaceappschallenge.org → your account → Team Thu's team page → Project tab → edit the project**. Paste each block into the matching field shown below. If the live wording differs, match its meaning. Review the complete entry together before the final submit action; the team must handle any terms acceptance.

## Project title

Flame in Freefall — NASA Fire Evidence Explorer

## High-level project summary / short description

Team Thu built a small dashboard that helps readers find and compare NASA fire experiments. Explore four investigations, compare reported conditions, and ask a fire safety question. Each evidence statement links to its NASA source. The prototype uses deterministic search, shows missing information and explains the limits of applying microgravity findings to the Moon or Mars.

## Detailed project description

Fire-safety research is spread across experiment catalogs and publications. Our prototype brings a small, traceable collection into one Python and Streamlit dashboard for students and researchers.

Explore filters BASS-II, SAME-R, FLEX and Saffire-II by prevention, detection or suppression. These categories are our relevance judgments. Compare places reported materials, oxygen concentration, airflow, pressure, sensors and measurements beside their sources and test context. Missing values are labeled “Not reported.” The app warns when study methods measure different things.

Ask ranks approved evidence using words and a documented synonym list, explains the matches, and displays a short selection of existing cited statements. For the question “Which NASA experiments can help us understand smoke detection in a spacecraft?”, SAME-R ranks first in our automated tests. Users can inspect its evidence and follow NASA links. Unrelated questions return a no-evidence message. This release does not call a language model; its evidence fallback needs no API key.

The structured collection contains catalog descriptions, publication abstracts and a NASA factsheet, not raw experiment files. Every claim records an evidence type, source, locator and context. The two smoke papers' different transport-time ranges remain separate. No numerical outcome chart or operational safety recommendation is inferred from incompatible methods.

AI assisted code, research extraction, tests and documentation. Automated tests cover the main workflows, missing values, unsupported questions, safe text rendering and a simulated failed optional-selector interface. Browser visual testing and signed-out public access remain unfinished. Teammate source review is pending. Microgravity evidence here cannot certify lunar or Martian fire-safety performance.

## NASA data resources / NASA data usage

We used NASA's PSI catalog records for BASS-II (PSI-25, DOI 10.60555/4qc4-de67), SAME-R (PSI-101, DOI 10.60555/2np7-jv14) and FLEX (PSI-69, DOI 10.60555/mbq8-0451). We combined these with NASA's Saffire factsheet and NTRS publication summaries. We did not download raw experiment files. Catalog objectives, published methods/results and team interpretations are labeled separately.

Paste the exact NASA bibliography from `docs/SOURCES.md` into the NASA Data/References field, preserving URLs, persistent identifiers and locators. The in-app Sources page provides the same source records. Check that at least one used source belongs to Flame in Freefall's official Resources list before claiming Global Awards eligibility.

## Space Agency and other data resources / References

No non-NASA scientific dataset was used. Tools: Python 3.12.14, Streamlit 1.67.0, Python unittest and Streamlit AppTest; pip-audit 2.10.1 and detect-secrets 1.5.0 for limited checks. OpenAI ChatGPT/Codex assisted development. Runtime dependency versions and license metadata are in `requirements.txt` and `docs/THIRD_PARTY.md`. NASA source rights are listed in `docs/SOURCES.md`. Team Thu's original code and paraphrases use the MIT License.

Tool sources: https://www.python.org/ ; https://docs.streamlit.io/ ; https://github.com/pypa/pip-audit ; https://github.com/Yelp/detect-secrets ; https://openai.com/chatgpt/ .

## Use of AI/SI tools

OpenAI ChatGPT/Codex substantially assisted research, source extraction, application code, tests and documentation. AI-authored data entries are paraphrases of cited NASA records, not generated measurements. Assistance is disclosed in the dataset metadata and AI-assistance log. Human teammate verification is pending. The running app uses deterministic evidence search and cited prewritten statements; it makes no external AI calls. No AI-generated images, audio or video are included.

## Link to project demo

**Missing — no demo recording or public demo URL has been created.** Confirm whether this field expects a video/slides demonstration under the current guide. Record the working journey after checking the allowed format and duration. Test the final link while signed out, then paste that actual URL. Do not paste a local `localhost` address.

## Link to final project

**Missing — no publicly deployed app or team-owned remote repository exists yet.** Deploy using `docs/DEPLOYMENT.md`, test the URL, then paste the live app URL. Add the actual source repository URL where the form requests it or in the detailed description/references. A downloadable source package is available to the team but has not been confirmed as a judge-accessible final-project link.

## Terms and conditions

The team must read the current terms, verify all claims and links, confirm local eligibility requirements, and review the complete rendered entry before accepting terms or submitting. No acceptance or submission has been performed.

## Demo narration — provisional short version

**The official duration is still unverified.** This 54-word draft is a rehearsal option of roughly 22–30 seconds, depending on speaking speed. It is not a claim of compliance. Rehearse with the actual clicks and adjust to the current guide.

“We are Team Thu. Our dashboard helps readers find NASA fire evidence. Ask about spacecraft smoke detection: SAME-R ranks first, with reasons and linked sources. Compare studies to see reported conditions and missing values. We preserve conflicting findings and explain method differences. This prototype uses deterministic search and summaries, not raw-data prediction or certification.”

Suggested screen actions: show the smoke question; click Find evidence; expand SAME-R; show a supporting NASA page; switch to Compare and point out Not reported. If source loading takes too long, prepare the already-open source tab for the recording. Use only tested features and verify the recording's public accessibility.

## Team review checklist

- [ ] Both teammates verify every scientific claim against its locator and update review status.
- [ ] Confirm Kathmandu schedule, creator timezone, registration and any earlier local deadline.
- [ ] Read current guide and official challenge resource list; confirm NASA resource eligibility.
- [ ] Record a demo within the verified format/limit; disclose any newly generated media.
- [ ] Test the hosted app on desktop and phone, including signed-out access and NASA links.
- [ ] Update actual privacy/host details, final links, validation status and AI disclosure.
- [ ] Review the completed Project tab before submitting; save the observed confirmation afterward.
