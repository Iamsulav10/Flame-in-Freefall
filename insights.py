"""Prepared interpretations linked to existing evidence, never generated measurements."""
from evidence import claim_ids_for, search_studies, study_by_id, tokens

INSIGHTS = {
    "same": {
        "title": "Smoke detection needs representative smoke",
        "interpretation": "Use this research to frame detector tests around smoke generation and transport conditions, rather than assuming one particle size represents every spacecraft fire.",
        "basis": ["same_detection", "same_result", "same_sample"],
        "gap": "The collection does not establish alarm thresholds, detection reliability or a certified detector choice. The two abstracts report different transport-time ranges.",
        "next_step": "Read the full methods and resolve the transport-time difference before designing a detector validation test."
    },
    "bass": {
        "title": "Connect solid-fuel burning with gas measurements",
        "interpretation": "Use BASS-II to investigate how solid-fuel test conditions and combustion-product measurements relate. Its heat-release summary is context for research, not a safe fire-size limit.",
        "basis": ["bass_purpose", "bass_sensors", "bass_result"],
        "gap": "The reviewed abstract does not provide the complete run-by-run gas and heat-release series.",
        "next_step": "Obtain the test matrix and match fuel geometry, oxygen and airflow before comparing runs."
    },
    "saffire": {
        "title": "Check conditions before transferring flame-spread results",
        "interpretation": "Use the PMMA comparison to examine the role of pressure and gravity in a specific material test. Do not turn it into a general conversion between Earth and spacecraft fire behavior.",
        "basis": ["saffire_result", "saffire_geometry", "saffire_flow"],
        "gap": "This is one material and method; it does not rank all spacecraft materials by safety.",
        "next_step": "Review the full paper and comparable material tests before extending the result to another geometry."
    },
    "flex": {
        "title": "Start with extinction questions, not suppressant prescriptions",
        "interpretation": "Use FLEX as a starting point for research into liquid-droplet extinction and gaseous suppression. The included catalog states study goals; it cannot establish which suppressant works best.",
        "basis": ["flex_purpose", "flex_suppress"],
        "gap": "No quantitative suppression outcome or fuel-specific test series is included.",
        "next_step": "Retrieve fuel-specific results and exposure constraints before considering a suppression design."
    },
}


def ranked_insights(question, data, category="All"):
    """Reuse the same transparent ranking as Ask; do not invent confidence scores."""
    return [(result, INSIGHTS[result.study_id])
            for result in search_studies(question, data, category)
            if result.study_id in INSIGHTS]


def ranking_breakdown(question, data, result):
    study = study_by_id(data, result.study_id)
    topic = tokens(" ".join(study["keywords"]) + " " + study["name"])
    topic_matches = tokens(question) & topic
    detail_matches = set(result.direct_matches) - topic_matches
    return {"Topic points": 4 * len(topic_matches),
            "Evidence-text points": 2 * len(detail_matches),
            "Related-term points": min(3, len(result.related_matches))}


def evidence_coverage(data, study):
    """Counts describe our collection, not the completeness of NASA's research."""
    refs = claim_ids_for(study)
    return {"Published statements": sum(data["claims"][ref]["evidence_type"] == "published_finding" for ref in refs),
            "Reported comparison fields": sum(bool(refs) for refs in study["fields"].values()),
            "Total comparison fields": len(study["fields"])}
