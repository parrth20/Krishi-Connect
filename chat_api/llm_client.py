import os

import requests


SYSTEM_PROMPT = """You are Krishi Connect, a practical farmer assistant.
Use only the supplied crop, disease, weather, and knowledge-base context.
Give a short actionable answer in simple language.
When chemicals are mentioned, tell the farmer to follow local registration, label dose, safety gear, and waiting period.
If context is not enough, ask for the missing crop, city, and symptom details.
"""


def _context_text(context):
    profile = context.get("profile")
    weather_summary = context.get("weather_summary") or {}
    current = weather_summary.get("current") or {}
    documents = context.get("documents") or []

    parts = []
    if profile:
        parts.append(f"Crop: {profile['crop']}")
        parts.append(f"Likely disease: {profile['disease']}")
        parts.append("Symptoms: " + "; ".join(profile["symptoms"]))
        parts.append("Cure steps: " + "; ".join(profile["cure"]))
        parts.append("Prevention: " + "; ".join(profile["prevention"]))
        parts.append("Weather risk: " + profile["weather_risk"])

    if current:
        parts.append(
            "Current weather: "
            f"{current.get('condition')}, "
            f"{current.get('temperature')} C, "
            f"{current.get('humidity')}% humidity, "
            f"{current.get('precipitation_probability')}% rain chance, "
            f"{current.get('wind_speed')} km/h wind."
        )

    if context.get("weather_advice"):
        parts.append("Farm weather advice: " + context["weather_advice"])

    if documents:
        parts.append("Retrieved knowledge:")
        for document in documents:
            parts.append(f"- {document['title']}: {document['body']}")

    return "\n".join(parts)


def llm_is_configured():
    return bool(os.getenv("CHAT_LLM_ENDPOINT"))


def generate_llm_answer(context):
    endpoint = os.getenv("CHAT_LLM_ENDPOINT")
    if not endpoint:
        return None

    model = os.getenv("CHAT_LLM_MODEL", "local-farmer-assistant")
    api_key = os.getenv("CHAT_LLM_API_KEY")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "temperature": 0.3,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Farmer question: {context.get('question')}\n\n"
                    f"City: {context.get('city') or 'not provided'}\n"
                    f"Crop hint: {context.get('crop') or 'not provided'}\n\n"
                    f"Context:\n{_context_text(context)}"
                ),
            },
        ],
    }

    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices") or []
        if choices:
            message = choices[0].get("message") or {}
            content = message.get("content")
            if content:
                return content.strip()
    except requests.RequestException:
        return None

    return None
