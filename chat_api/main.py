from typing import List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from chatBackend.rag_service import build_chat_context, compose_dynamic_answer
from weatherapp.services import get_weather_summary

from .llm_client import generate_llm_answer, llm_is_configured


class ChatRequest(BaseModel):
    message: str
    city: Optional[str] = ""
    crop: Optional[str] = ""
    disease: Optional[str] = ""
    use_llm: bool = True


class ChatSource(BaseModel):
    id: str
    title: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[ChatSource]
    provider: str
    used_weather: bool
    used_llm: bool


app = FastAPI(title="Krishi Connect Farmer Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _should_fetch_weather(message):
    message = (message or "").lower()
    return any(
        word in message
        for word in ["weather", "rain", "spray", "humidity", "temperature", "wind", "mausam"]
    )


def _sources_from_context(context):
    sources = []
    profile = context.get("profile")
    if profile:
        sources.append({"id": profile["slug"], "title": f"{profile['crop']} - {profile['disease']}"})

    for document in context.get("documents") or []:
        sources.append({"id": document["id"], "title": document["title"]})

    unique = []
    seen = set()
    for source in sources:
        if source["id"] not in seen:
            unique.append(source)
            seen.add(source["id"])
    return unique[:4]


@app.get("/health")
def health():
    return {"status": "ok", "llm_configured": llm_is_configured()}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    weather_summary = None
    if request.city and _should_fetch_weather(request.message):
        weather_summary = get_weather_summary(request.city)

    context = build_chat_context(
        request.message,
        city=request.city or "",
        crop=request.crop or "",
        disease_slug=request.disease or "",
        weather_summary=weather_summary,
    )

    answer = None
    used_llm = False
    if request.use_llm:
        answer = generate_llm_answer(context)
        used_llm = bool(answer)

    if not answer:
        answer = compose_dynamic_answer(context)

    return {
        "answer": answer,
        "sources": _sources_from_context(context),
        "provider": "fastapi-llm-rag" if used_llm else "fastapi-local-rag",
        "used_weather": bool(weather_summary and not weather_summary.get("error")),
        "used_llm": used_llm,
    }
