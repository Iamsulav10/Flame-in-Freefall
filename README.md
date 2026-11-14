# Flame in Freefall

A NASA fire research dashboard by **Team Thu**, Kathmandu, Nepal.

We are a team of two beginners building this project for the **2026 NASA Space Apps Challenge**. Flame in Freefall uses Python and Streamlit to help people explore NASA research about fire in space.

The idea is simple: find a relevant experiment, look at its conditions, and open the original source to learn more.

## Why we made this

NASA has research on how flames spread, how smoke moves, and how fires can be extinguished in microgravity. That information is spread across different pages, abstracts and reports. It can be difficult to know where to start or whether two experiments can be compared fairly.

We brought a small collection of this research into one dashboard. Our goal is to make it easier for students and other interested readers to find useful information and check where it came from.

## What you can do

- **Explore:** Browse four investigations and filter them by prevention, detection or suppression.
- **Compare:** Choose two investigations and view their reported conditions side by side, including fuel samples, oxygen, airflow, pressure and measurements. Missing details are shown as “Not reported.”
- **Ask:** Type a question in English to find related investigations and short evidence statements with citations.
- **Check sources:** Follow the NASA links and read about the limits of the information we included.

Our categories and search rankings help people browse the research. They are our interpretations, not NASA safety ratings.

## Research included

The collection contains **4 investigations, 30 evidence claims and 9 NASA sources**.

| Investigation | What it covers | Source |
|---|---|---|
| BASS-II | Ignition, flame spread and extinction in solid fuels | [NASA PSI-25](https://psi.nasa.gov/physci/repo/data/investigations/PSI-25) |
| SAME-R | Smoke particles and the conditions in which they form and travel | [NASA PSI-101](https://psi.nasa.gov/physci/repo/data/investigations/PSI-101) |
| FLEX | Research objectives for liquid-droplet flammability and extinguishment | [NASA PSI-69](https://psi.nasa.gov/physci/repo/data/investigations/PSI-69) |
| Saffire-II | Material flammability and a published flame-spread comparison | [NASA NTRS](https://ntrs.nasa.gov/citations/20200000557) |

We used NASA catalog descriptions, publication abstracts and a factsheet. **We did not download or analyze raw experiment data.** Each evidence claim includes its source, context and review status.

Some sources report different values. For example, two smoke abstracts give transport-time ranges of 11–1800 seconds and 11–800 seconds. We keep both with their citations because we have not yet checked the full methods to explain the difference.

The full references are in [SOURCES.md](docs/SOURCES.md). The collected evidence is in [data/evidence.json](data/evidence.json).

## A quick example

Open **Ask** and enter:

> Which NASA experiments can help us understand smoke detection in a spacecraft?

1. Click **Find evidence**.
2. Read the matching investigations and the reasons they appear. SAME-R ranks first in the recorded automated test.
3. Expand **Inspect SAME-R** to read its evidence and limitations.
4. Open a source link to check the original information.
5. Go to **Compare** and choose SAME-R and Saffire-II to see how their methods and reported conditions differ.

This helps you find research. It does not tell you which smoke detector is safe to use in a spacecraft.

## How the search works

The Ask feature matches keywords and related terms against the records in our collection. It ranks the matches and returns up to three existing evidence statements with citations. If a question has little or no support in the collection, the app explains that limit.

**The app does not call an AI model and does not need an API key.** A higher search score means a closer text match, not stronger scientific evidence.

## Run it on your computer

Python **3.12** was used for the recorded automated tests. Download and extract the repository, then open a terminal in the folder containing `app.py` and `requirements.txt`.

### Windows

Run these commands one at a time in Terminal or PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

### macOS or Linux

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Open the address shown in the terminal, usually `http://localhost:8501`. Keep the terminal open while using the app. Press **Ctrl+C** to stop it.

Start the app from the project folder so it can read `.streamlit/config.toml`.

### Run the tests

On Windows:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On macOS or Linux:

```sh
.venv/bin/python -m unittest discover -s tests -v
```

For hosting instructions, see [DEPLOYMENT.md](docs/DEPLOYMENT.md). The repository is now available [on GitHub](https://github.com/Iamsulav10/Flame-in-Freefall), so the earlier note in that guide about not having a repository is out of date.

## Current progress and limits

The prototype runs locally. A public demo link has not yet been verified.

The packaged release recorded **23 passing automated tests** with Python 3.12.14 and Streamlit 1.67.0, plus a local HTTP startup check. The tests cover search, comparisons, missing values, filters and input handling. The recorded dependency audit found no known advisories in the 34 pinned runtime packages, and secret scans found no confirmed credentials. These checks do not guarantee security. Details are in [VALIDATION.md](reports/VALIDATION.md).

There is still work to do:

- Have a teammate verify each source claim.
- Check the full experience on desktop and mobile, including opening the external sources.
- Verify that a public deployment works without signing in.

The collection is small and does not cover all NASA fire research. FLEX currently includes objectives and methods, not an extracted quantitative result. Different fuels and experiment conditions also mean that results cannot always be compared directly.

The dashboard is a student research tool. It cannot monitor fires, give emergency instructions or certify equipment. Microgravity findings alone also cannot establish safe settings for the Moon or Mars.

## Privacy

The app has no accounts, file uploads, advertising or query database. Questions are processed in the server session. Optional Streamlit usage reporting is disabled, and CORS and XSRF protections remain enabled.

Cookies, analytics and data retention still need to be checked for the actual hosting service. More information is in [PRIVACY_SECURITY.md](docs/PRIVACY_SECURITY.md).

## About our use of AI

We used **OpenAI ChatGPT/Codex** for substantial help with research, source extraction, programming, tests and documentation. We have recorded that assistance in [AI_ASSISTANCE.md](docs/AI_ASSISTANCE.md).

The scientific measurements were not AI-generated. Our use of AI during development is separate from the app's keyword-based search.

## Project files

| File or folder | Purpose |
|---|---|
| `app.py` | Dashboard pages and controls |
| `evidence.py` | Evidence validation, search and ranking |
| `data/evidence.json` | Research records, claims and sources |
| `.streamlit/config.toml` | Theme and Streamlit settings |
| `tests/` | Automated checks |
| `docs/` | Sources, setup instructions and project notes |
| `reports/` | Validation results |

To understand the project in more detail, see [Explain the project to judges](docs/EXPLAIN_TO_JUDGES.md). To add a verified study, see the [data dictionary](docs/DATA_DICTIONARY.md).

## License and credits

Our original code and paraphrases use the [MIT License](LICENSE). NASA records and third-party publications keep their own rights. See [source rights](docs/SOURCES.md) and [dependency licenses](docs/THIRD_PARTY.md).

No NASA logos, source images or source PDFs are included. This project is not endorsed by NASA.
