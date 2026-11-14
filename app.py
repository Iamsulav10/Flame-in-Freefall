"""Team Thu's Streamlit interface. Scientific content lives in data/evidence.json."""

import time
from pathlib import Path

import streamlit as st

from evidence import (
    FIELD_LABELS, MAX_QUESTION_LENGTH, answer_question, claim_ids_for,
    comparison_warnings, load_data, rate_allowed, search_studies, study_by_id,
)

DEMO_QUESTION = "Which NASA experiments can help us understand smoke detection in a spacecraft?"
ROOT = Path(__file__).parent
TYPE_LABELS = {
    "experiment_record": "Experiment record / stated approach",
    "published_finding": "Published finding / reported method",
    "hypothesis": "Hypothesis, not a result",
    "interpretation": "Team/AI interpretation",
}


def render_claim(data, claim_id, show_context=True):
    claim = data["claims"][claim_id]
    source = data["sources"][claim["source_id"]]
    # Plain text prevents evidence or future user text from becoming active HTML.
    st.text(claim["text"])
    st.link_button(f"Source: {claim['source_id']} · {claim['locator']}", source["url"])
    if show_context:
        st.caption(TYPE_LABELS[claim["evidence_type"]])
        st.text(claim["context"])


def render_study(data, study, expanded=False):
    with st.expander(f"Inspect {study['name']} · {study['title']}", expanded=expanded):
        st.caption(" / ".join(study["categories"]) + " · Team relevance classification")
        render_claim(data, study["purpose"])
        st.text(study["scope"])
        st.markdown("**What the included sources report**")
        if study["findings"]:
            for claim_id in study["findings"]:
                render_claim(data, claim_id)
        else:
            st.text("No quantitative finding extracted. The included catalog describes objectives and methods.")
        if study["id"] == "flex":
            render_claim(data, "flex_suppress")
        if study["id"] == "same":
            st.warning(data["discrepancies"][0]["note"])
            for ref in data["discrepancies"][0]["claim_ids"]:
                render_claim(data, ref)
        st.markdown("**Evidence access**")
        for source_id in study["source_ids"]:
            source = data["sources"][source_id]
            st.text(source["title"])
            st.text(source["persistent_id"])
            st.text(source["access_level"])
            st.link_button(f"Open NASA record · {source_id}", source["url"])


def ask_page(data):
    st.header("Ask a fire safety question")
    st.write("Find relevant experiments, read the evidence, and open the NASA source.")
    st.caption("Local evidence search. No generative AI service is connected; questions are not sent to an AI provider.")
    with st.form("question_form"):
        question = st.text_area("Your question", value=DEMO_QUESTION,
                                max_chars=MAX_QUESTION_LENGTH, height=110,
                                help="Use a topic such as smoke, flame spread or droplet extinction. Do not enter personal information.")
        submitted = st.form_submit_button("Find evidence", type="primary")
    if submitted:
        if not question.strip():
            st.session_state.pop("answer", None)
            st.info("Enter a fire safety topic to search.")
        else:
            allowed, history = rate_allowed(st.session_state.get("requests", []), time.monotonic())
            st.session_state["requests"] = history
            if allowed:
                try:
                    st.session_state["answer"] = answer_question(question, data)
                    st.session_state["asked_question"] = question
                except ValueError:
                    st.session_state.pop("answer", None)
                    st.error("Please use a question of 600 characters or fewer.")
            else:
                st.info("Please wait a moment. You can make up to 10 searches per minute in this session.")
    response = st.session_state.get("answer")
    if not response:
        return
    st.divider()
    st.subheader("Evidence summary")
    st.text(st.session_state["asked_question"])
    st.caption(response["mode"])
    if response["notice"]:
        st.info(response["notice"])
    for ref in response["claim_ids"]:
        render_claim(data, ref)
    if response["results"]:
        st.subheader("Matching investigations")
        st.caption("Scores count topic matches. They are not scientific confidence, risk or detector-performance scores.")
    for position, result in enumerate(response["results"], 1):
        study = study_by_id(data, result.study_id)
        st.markdown(f"**{position}. {study['name']}** · Relevance score {result.score}")
        st.text("Matches: " + ", ".join(result.direct_matches))
        if result.related_matches:
            st.text("Related terms: " + ", ".join(result.related_matches))
        render_study(data, study)


def explore_page(data):
    st.header("Explore investigations")
    category = st.selectbox("Fire safety purpose", ["All", "Prevention", "Detection", "Suppression"])
    query = st.text_input("Search investigations", max_chars=MAX_QUESTION_LENGTH,
                          placeholder="Smoke, PMMA, droplet extinction…")
    if query.strip():
        matches = search_studies(query, data, category)
        studies = [study_by_id(data, result.study_id) for result in matches]
    else:
        studies = [study for study in data["studies"] if category == "All" or category in study["categories"]]
    st.caption(f"{len(studies)} of 4 investigations · Categories are Team Thu's interpretation")
    if not studies:
        st.info("No match in this collection. Clear the search or choose another purpose.")
    for study in studies:
        with st.container(border=True):
            st.subheader(study["name"])
            render_claim(data, study["purpose"], show_context=False)
            st.caption(study["scope"])
            render_study(data, study)


def compare_page(data):
    st.header("Compare methods and conditions")
    st.write("Read what each source reports before comparing outcomes.")
    ids = [study["id"] for study in data["studies"]]
    names = {study["id"]: study["name"] for study in data["studies"]}
    left_id = st.selectbox("First investigation", ids, index=1, format_func=names.get)
    right_id = st.selectbox("Second investigation", [i for i in ids if i != left_id], format_func=names.get)
    left, right = study_by_id(data, left_id), study_by_id(data, right_id)
    for warning in comparison_warnings(left, right):
        st.info(warning)
    st.caption("Not reported = not stated in the included sources. It does not mean zero or absent from all NASA records.")
    # Each field is a short, wrapping pair rather than a wide table that needs
    # horizontal scrolling on a phone. Original units are deliberately retained.
    for field, label in FIELD_LABELS.items():
        st.subheader(label)
        columns = st.columns(2, border=True, wrap=True)
        for column, study in zip(columns, (left, right)):
            with column:
                st.markdown(f"**{study['name']}**")
                references = study["fields"][field]
                if not references:
                    st.text("Not reported")
                for ref in references:
                    render_claim(data, ref)
    if "same" in {left_id, right_id}:
        st.warning(data["discrepancies"][0]["note"])
    st.caption("No outcome chart is shown: these sources do not provide a common, comparable measurement series.")


def about_page(data):
    st.header("Sources, limits and privacy")
    st.subheader("What this collection contains")
    st.write("Four investigations, with short paraphrases of NASA catalog records and publications. No raw experiment files were downloaded or analyzed. Human teammate verification of every claim is still pending.")
    render_claim(data, data["global_limit_claim"])
    st.write("The Moon and Mars have partial gravity. These microgravity records can guide further research; they cannot certify a detector or supply operational fire-response instructions.")
    st.subheader("How answers work")
    st.write("Words and a small, documented synonym list rank the four studies. The answer displays up to three existing evidence statements with their citations. It does not generate new scientific claims. Search scores measure word relevance only.")
    st.subheader("Privacy and cookies")
    st.write("Questions are processed by the Python server and kept in the current Streamlit session. This app does not intentionally save questions to files, databases or application logs. It has no accounts, uploads, advertising or app analytics. Do not enter personal or confidential information.")
    st.write("No external AI provider is configured or called. Optional Streamlit usage reporting is disabled. Streamlit's security protections remain enabled and may set a security cookie. Hosting providers may keep connection logs and analytics; no public host has been verified for this release. A host's retention and cookie behavior must be checked before publication.")
    st.link_button("Streamlit configuration and cookie settings", "https://docs.streamlit.io/develop/api-reference/configuration/config.toml")
    st.link_button("Community Cloud viewer analytics", "https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/app-analytics")
    st.subheader("Sources and licenses")
    st.write("Team Thu's original code and paraphrases are MIT licensed. Upstream materials retain their own rights. No NASA logos, source PDFs or source images are bundled. This student project is not endorsed by NASA.")
    for source_id, source in data["sources"].items():
        with st.expander(f"{source_id} · {source['title']}"):
            for key in ("persistent_id", "access_level", "license", "checked_on"):
                st.text(f"{key.replace('_', ' ').capitalize()}: {source[key]}")
            st.link_button(f"Open source {source_id}", source["url"])
    st.subheader("AI assistance")
    st.write("OpenAI ChatGPT/Codex assisted research, source extraction, code, tests and documentation. Scientific measurements were not generated. Build work began after the event opening. See the packaged AI assistance log for work performed and pending human review.")


def main():
    st.set_page_config(page_title="Flame in Freefall · Team Thu", layout="wide")
    st.title("Flame in Freefall")
    st.caption("Team Thu · NASA combustion evidence")
    try:
        data = load_data()
    except (ValueError, KeyError, OSError, TypeError):
        st.error("The evidence collection could not be loaded. Please contact the project team.")
        st.stop()
    page = st.radio("Workspace", ["Ask", "Explore", "Compare", "Sources & privacy"], horizontal=True, label_visibility="collapsed")
    st.divider()
    {"Ask": ask_page, "Explore": explore_page, "Compare": compare_page,
     "Sources & privacy": about_page}[page](data)
    st.divider()
    st.caption("Evidence discovery for learning and research. Published summaries, not spacecraft safety certification.")


if __name__ == "__main__":
    main()
