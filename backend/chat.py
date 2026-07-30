from fastapi import APIRouter
from pydantic import BaseModel

from rag import search_chunks
from gemini import ask_gemini

router = APIRouter()


class Question(BaseModel):
    question: str


@router.post("/chat")
def chat(data: Question):

    docs = search_chunks(data.question)

    context = ""

    sources = []

    for doc in docs:
        context += doc.page_content + "\n\n"

        if "source" in doc.metadata:
            sources.append(doc.metadata["source"])

    try:
        answer = ask_gemini(data.question, context)
        gemini_status = True

    except Exception as e:
        print("Gemini Error:", e)

        answer = (
            "⚠️ Gemini API quota exceeded or unavailable.\n\n"
            "Retrieved information from the uploaded document:\n\n"
            f"{context}"
        )

        gemini_status = False

    return {
        "question": data.question,
        "answer": answer,
        "sources": list(set(sources)),
        "gemini": gemini_status
    }