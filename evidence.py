"""Small, offline evidence search. No model, network, or secret access here."""

import json
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

MAX_QUESTION_LENGTH = 600
DATA_PATH = Path(__file__).parent / "data" / "evidence.json"
ALLOWED_HOSTS = {"psi.nasa.gov", "ntrs.nasa.gov", "www.nasa.gov"}
FIELD_LABELS = {
    "sample": "Fuel or sample",
    "oxygen": "Oxygen concentration",
    "airflow": "Airflow",
    "pressure": "Pressure",
    "geometry": "Sample dimensions",
    "sensors": "Sensors and diagnostics",
    "measurements": "Measurements",
    "transport_time": "Smoke transport time",
}
STOP_WORDS = set("which what when how why can could would should do does did is are was were the a an and or for to in on of us we me help understand about nasa experiments experiment studies study spacecraft space station research please tell show find use using used with from that this it its".split())
ALIASES = {
    "detect": "detection", "detectors": "detector", "detecting": "detection",
    "alarms": "alarm", "particles": "particle", "aerosols": "aerosol",
    "sensors": "sensor", "fuels": "fuel", "solids": "solid",
    "droplets": "droplet", "materials": "material", "fires": "fire",
    "extinguishing": "extinction", "extinguish": "extinction",
    "suppress": "suppression", "suppressants": "suppressant",
    "burning": "combustion", "flows": "airflow", "flow": "airflow",
    "ventilation": "airflow", "pmma": "acrylic",
}
RELATED = (
    {"smoke", "aerosol", "particle", "detector", "detection", "alarm"},
    {"suppression", "suppressant", "extinction"},
    {"liquid", "droplet"},
    {"solid", "material", "acrylic"},
)
SCOPE_TERMS = {"safe", "safest", "dose", "dosage", "threshold", "certify", "certified", "recommend", "best", "mars", "lunar", "moon"}
SCOPE_NOTICE = "Related studies found, but this collection cannot establish safe operating settings, choose a certified detector, or predict lunar/Martian performance. The evidence below is background only."


def tokens(text):
    """Normalize words without requiring a language-model service."""
    return {ALIASES.get(word, word) for word in re.findall(r"[a-z0-9]+", text.lower())} - STOP_WORDS


def is_approved_url(url):
    parts = urlsplit(url)
    return (parts.scheme == "https" and parts.hostname in ALLOWED_HOSTS
            and parts.username is None and parts.password is None and parts.port is None)


def validate_data(data):
    """Fail closed if an edited record loses provenance or introduces another host."""
    if data["schema_version"] != 1 or data["raw_data_downloaded"] is not False:
        raise ValueError("Unsupported evidence format")
    for source in data["sources"].values():
        if not is_approved_url(source["url"]):
            raise ValueError("Unapproved evidence URL")
        for field in ("title", "persistent_id", "access_level", "license", "checked_on"):
            if not source.get(field):
                raise ValueError("Incomplete source")
    for claim in data["claims"].values():
        if claim["source_id"] not in data["sources"] or not claim["locator"] or not claim["context"]:
            raise ValueError("Claim has no supporting source or context")
        if claim["evidence_type"] not in {"experiment_record", "published_finding", "hypothesis", "interpretation"}:
            raise ValueError("Unknown evidence type")
        quantity = claim["quantity"]
        if quantity and not quantity.get("unit"):
            raise ValueError("Numeric claim needs units")
    ids = set()
    for study in data["studies"]:
        if study["id"] in ids or set(study["fields"]) != set(FIELD_LABELS):
            raise ValueError("Invalid study fields or duplicate ID")
        ids.add(study["id"])
        references = [study["purpose"], *study["findings"]]
        references += [ref for refs in study["fields"].values() for ref in refs]
        for reference in references:
            if reference not in data["claims"]:
                raise ValueError("Unknown claim")
            if data["claims"][reference]["source_id"] not in study["source_ids"]:
                raise ValueError("Claim source is missing from study")
    return data


def load_data(path=DATA_PATH):
    return validate_data(json.loads(Path(path).read_text(encoding="utf-8")))


@dataclass(frozen=True)
class SearchResult:
    study_id: str
    score: int
    direct_matches: tuple
    related_matches: tuple


def search_studies(question, data, category="All"):
    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError("Please use 600 characters or fewer.")
    query = tokens(question)
    if not query:
        return []
    expanded = set().union(*(group for group in RELATED if group & query)) if query else set()
    results = []
    for study in data["studies"]:
        if category != "All" and category not in study["categories"]:
            continue
        topic = tokens(" ".join(study["keywords"]) + " " + study["name"])
        detail = tokens(" ".join(data["claims"][ref]["text"] for ref in claim_ids_for(study)))
        direct = query & topic
        detail_matches = (query & detail) - direct
        related = (expanded & topic) - direct
        # A real topic match must anchor every result. Synonyms alone cannot
        # pull a different investigation into an unrelated question.
        if not direct and not detail_matches:
            continue
        score = 4 * len(direct) + 2 * len(detail_matches) + min(3, len(related))
        results.append(SearchResult(study["id"], score, tuple(sorted(direct | detail_matches)), tuple(sorted(related))))
    return sorted(results, key=lambda result: (-result.score, result.study_id))


def study_by_id(data, study_id):
    return next(study for study in data["studies"] if study["id"] == study_id)


def claim_ids_for(study):
    return list(dict.fromkeys([study["purpose"], *study["findings"],
                              *(ref for refs in study["fields"].values() for ref in refs)]))


def comparison_warnings(left, right):
    warnings = ["These studies use different materials and methods. Their measurements are not a shared performance scale.",
                "A catalog capability or planned range is not a measured test result. Read the condition beside each value."]
    if "same" in {left["id"], right["id"]}:
        warnings.append("SAME-R examines smoke from samples heated below ignition. Its particle sizes cannot be compared directly with flame-spread or extinction outcomes.")
    return warnings


def rate_allowed(previous_times, now):
    """A small session throttle; not an IP-level denial-of-service defense."""
    recent = [value for value in previous_times if now - value < 60]
    allowed = len(recent) < 10 and (not recent or now - recent[-1] >= 2)
    return allowed, recent + [now] if allowed else recent


def answer_question(question, data, selector=None):
    """Return cited, prewritten evidence. An optional future selector may choose
    approved claim IDs only; it cannot supply new text, tools, or URLs.
    There is no external provider implementation in this release.
    """
    results = search_studies(question, data)
    response = {"mode": "Evidence summary · no generative AI", "results": results,
                "claim_ids": [], "notice": "", "selector_failed": False}
    if not results:
        response["notice"] = "No matching evidence in these four studies. Try smoke detection, solid flame spread, or droplet extinction. This is a small collection, not all NASA research."
        return response
    query = tokens(question)
    matched = set().union(*(set(result.direct_matches) for result in results))
    coverage = len(query & matched) / len(query)
    if coverage < 0.6:
        response["notice"] = (SCOPE_NOTICE if query & SCOPE_TERMS else
                              "Only a small part of this question matches the collection. The evidence is too weak to answer it. Related studies are listed below for inspection.")
        return response
    if coverage < 0.75:
        response["notice"] = "Only part of this question matches the collection. These related statements are background, not a complete answer."
    selected = [r for r in results[:2] if r.score >= results[0].score * 0.6]
    candidates = []
    for result in selected:
        study = study_by_id(data, result.study_id)
        candidates.extend(claim_ids_for(study))
    # Keep the purpose first, then the most relevant available findings/details.
    first = study_by_id(data, results[0].study_id)["purpose"]
    ranked = sorted((ref for ref in candidates if ref != first),
                    key=lambda ref: (-len(tokens(data["claims"][ref]["text"]) & query),
                                     data["claims"][ref]["evidence_type"] != "published_finding",
                                     candidates.index(ref)))
    chosen = [first, *ranked[:2]]
    if selector is not None:
        try:
            proposed = selector(question, {ref: data["claims"][ref] for ref in candidates})
            if (not isinstance(proposed, list) or not 1 <= len(proposed) <= 3
                    or any(not isinstance(ref, str) or ref not in candidates for ref in proposed)):
                raise ValueError("Selector must return approved claim IDs")
            chosen = list(dict.fromkeys(proposed))
        except Exception:
            # Never expose a provider exception: it might contain a key or input.
            response["selector_failed"] = True
            response["notice"] = "Optional selector unavailable. Showing the same local evidence summary."
    response["claim_ids"] = chosen
    if query & SCOPE_TERMS:
        response["notice"] = SCOPE_NOTICE
    return response
