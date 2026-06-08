import math
import re
from collections import Counter

from .farmer_knowledge import DISEASE_PROFILES, KNOWLEDGE_DOCUMENTS, SAMPLE_CASES


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "for", "from",
    "has", "have", "how", "i", "in", "is", "it", "me", "my", "of", "on", "or",
    "please", "should", "tell", "that", "the", "this", "to", "what", "when",
    "where", "which", "with", "you", "your",
}


def _tokenize(text):
    return [
        token
        for token in re.findall(r"[a-zA-Z0-9]+", (text or "").lower())
        if token not in STOP_WORDS and len(token) > 1
    ]


def _cosine_score(query_tokens, document_tokens):
    if not query_tokens or not document_tokens:
        return 0

    q_count = Counter(query_tokens)
    d_count = Counter(document_tokens)
    common = set(q_count) & set(d_count)
    numerator = sum(q_count[word] * d_count[word] for word in common)
    q_norm = math.sqrt(sum(value * value for value in q_count.values()))
    d_norm = math.sqrt(sum(value * value for value in d_count.values()))
    if not q_norm or not d_norm:
        return 0
    return numerator / (q_norm * d_norm)


def retrieve_documents(question, limit=3):
    query_tokens = _tokenize(question)
    scored = []

    for document in KNOWLEDGE_DOCUMENTS:
        searchable = f"{document['title']} {document.get('topic', '')} {document['body']}"
        score = _cosine_score(query_tokens, _tokenize(searchable))
        if score > 0:
            scored.append((score, document))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [document for _, document in scored[:limit]]


def profile_to_context(profile):
    cure = " ".join(profile["cure"])
    symptoms = " ".join(profile["symptoms"])
    prevention = " ".join(profile["prevention"])
    return f"{profile['crop']} {profile['disease']}. Symptoms: {symptoms}. Cure: {cure}. Prevention: {prevention}"


def get_sample_cases():
    cases = []
    for case in SAMPLE_CASES:
        profile = DISEASE_PROFILES[case["slug"]]
        cases.append({**case, **profile})
    return cases


def get_disease_profile(slug):
    return DISEASE_PROFILES.get(slug)


def detect_disease(crop_hint="", symptoms="", filename="", plant_name=""):
    text = " ".join([crop_hint or "", symptoms or "", filename or "", plant_name or ""]).lower()
    if not text.strip():
        return {**DISEASE_PROFILES["leaf-stress"], "reason": "No crop or symptom details were provided."}

    scored = []
    for slug, profile in DISEASE_PROFILES.items():
        if slug == "leaf-stress":
            continue
        score = 0
        for keyword in profile.get("keywords", []):
            if keyword in text:
                score += 2 if keyword in profile["disease"].lower() else 1
        crop = profile["crop"].lower()
        if crop in text:
            score += 2
        if score:
            scored.append((score, profile))

    if scored:
        scored.sort(key=lambda item: item[0], reverse=True)
        profile = dict(scored[0][1])
        profile["confidence"] = min(0.95, profile.get("confidence", 0.8) + scored[0][0] * 0.01)
        profile["reason"] = "Matched crop and symptom keywords from the upload details."
        return profile

    profile = dict(DISEASE_PROFILES["leaf-stress"])
    profile["reason"] = "The upload did not match one of the preloaded disease patterns, so general leaf-stress guidance is shown."
    return profile


def disease_answer(profile):
    lines = [
        f"Possible diagnosis: {profile['disease']} in {profile['crop']}.",
        f"Confidence: {round(profile.get('confidence', 0.5) * 100)}%.",
        "",
        "What to do now:",
    ]
    lines.extend(f"- {item}" for item in profile["cure"])
    lines.append("")
    lines.append("Prevent next time:")
    lines.extend(f"- {item}" for item in profile["prevention"])
    lines.append("")
    lines.append(f"Weather risk: {profile['weather_risk']}")
    return "\n".join(lines)


def weather_advice(weather_summary):
    if not weather_summary or weather_summary.get("error"):
        return ""

    current = weather_summary.get("current", {})
    rain_chance = current.get("precipitation_probability")
    humidity = current.get("humidity")
    wind_speed = current.get("wind_speed")
    temperature = current.get("temperature")
    advice = []

    if rain_chance is not None and rain_chance >= 60:
        advice.append("Rain chance is high, so avoid spraying and check drainage.")
    elif rain_chance is not None and rain_chance >= 35:
        advice.append("Rain is possible; spray only if you have a dry 6-8 hour window.")

    if humidity is not None and humidity >= 85:
        advice.append("Humidity is high, so fungal diseases can spread faster.")

    if wind_speed is not None and wind_speed >= 20:
        advice.append("Wind is strong for spraying; wait for calmer conditions.")

    if temperature is not None and temperature >= 35:
        advice.append("Heat stress risk is high; irrigate early morning or evening.")

    if not advice:
        advice.append("Weather looks usable for field inspection and routine crop work.")

    return " ".join(advice)


def _find_profile_from_text(text):
    text = (text or "").lower()
    for profile in DISEASE_PROFILES.values():
        if profile["disease"].lower() in text or profile["crop"].lower() in text:
            keyword_hits = sum(1 for keyword in profile.get("keywords", []) if keyword in text)
            if keyword_hits or "cure" in text or "disease" in text:
                return profile
    return None


def _question_focus(question):
    question = (question or "").lower()
    return {
        "asks_cure": any(word in question for word in ["cure", "treat", "solution", "medicine", "recover", "control"]),
        "asks_spray": any(word in question for word in ["spray", "fungicide", "pesticide", "chemical"]),
        "asks_weather": any(word in question for word in ["weather", "rain", "humidity", "temperature", "wind", "mausam"]),
        "asks_symptoms": any(word in question for word in ["symptom", "identify", "detect", "spot", "yellow", "brown", "leaf"]),
        "asks_prevention": any(word in question for word in ["prevent", "avoid", "next time", "future"]),
    }


def build_chat_context(question, city="", crop="", disease_slug="", weather_summary=None):
    question = (question or "").strip()
    profile = get_disease_profile(disease_slug) if disease_slug else None
    profile = profile or _find_profile_from_text(" ".join([question, crop or ""]))

    retrieval_query = " ".join(
        part
        for part in [question, crop or "", profile_to_context(profile) if profile else ""]
        if part
    )
    documents = retrieve_documents(retrieval_query, limit=4)

    return {
        "question": question,
        "city": city,
        "crop": crop,
        "profile": profile,
        "documents": documents,
        "weather_summary": weather_summary,
        "weather_advice": weather_advice(weather_summary),
        "focus": _question_focus(question),
    }


def compose_dynamic_answer(context):
    question = context.get("question", "")
    if not question:
        return "Ask me about a crop disease, cure, irrigation, spraying, or local weather."

    profile = context.get("profile")
    documents = context.get("documents", [])
    focus = context.get("focus", {})
    weather_note = context.get("weather_advice")

    if profile:
        lines = [
            f"For {profile['crop']}, this looks closest to {profile['disease']}.",
            f"Confidence from the available crop context: {round(profile.get('confidence', 0.5) * 100)}%.",
        ]

        if focus.get("asks_symptoms") or not any(focus.values()):
            lines.append("")
            lines.append("Compare these symptoms:")
            lines.extend(f"- {item}" for item in profile["symptoms"][:3])

        if focus.get("asks_cure") or focus.get("asks_spray") or not any(focus.values()):
            lines.append("")
            lines.append("Do this first:")
            lines.extend(f"- {item}" for item in profile["cure"])

        if focus.get("asks_prevention") or not any(focus.values()):
            lines.append("")
            lines.append("To prevent repeat infection:")
            lines.extend(f"- {item}" for item in profile["prevention"])

        if focus.get("asks_spray"):
            lines.append("")
            lines.append("Spray caution:")
            lines.append("- Spray only in calm weather with a dry 6-8 hour window.")
            lines.append("- Use only locally approved products and follow label dose, safety gear, and waiting period.")

        lines.append("")
        lines.append(f"Disease-weather link: {profile['weather_risk']}")
    elif documents:
        lines = [
            "I found these relevant farm-care points from the knowledge base:",
        ]
        for document in documents[:3]:
            lines.append(f"- {document['body']}")
        lines.append("")
        lines.append("For a sharper answer, add crop name, city, leaf symptoms, and whether the spots are spreading.")
    else:
        lines = [
            "I need a little more crop context to answer safely.",
            "Send crop name, city, symptoms, and whether the problem is on leaves, stem, fruit, or roots.",
        ]

    if weather_note:
        location = (context.get("weather_summary") or {}).get("location", {}).get("name") or context.get("city")
        lines.append("")
        lines.append(f"Weather note for {location}: {weather_note}")

    return "\n".join(lines)


def answer_farmer_question(question, city="", crop="", disease_slug="", weather_summary=None):
    context = build_chat_context(
        question,
        city=city,
        crop=crop,
        disease_slug=disease_slug,
        weather_summary=weather_summary,
    )
    profile = context.get("profile")
    documents = context.get("documents", [])
    sources = [{"id": doc["id"], "title": doc["title"]} for doc in documents]
    if profile:
        sources.insert(0, {"id": profile["slug"], "title": f"{profile['crop']} - {profile['disease']}"})

    return {
        "answer": compose_dynamic_answer(context),
        "sources": sources[:4],
    }
