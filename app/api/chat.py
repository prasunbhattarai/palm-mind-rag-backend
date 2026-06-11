import json

from fastapi import APIRouter
from pydantic import BaseModel

from app.db.redis import get_client
from app.services.rag import search_documents
from app.services.booking import create_booking
from app.services.llm import generate_response, extract_booking_info

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


def get_history(session_id: str):
    data = get_client().get(f"session:{session_id}")
    return json.loads(data) if data else []


def save_history(session_id: str, history: list):
    get_client().set(f"session:{session_id}", json.dumps(history))


@router.post("/chat")
def chat(req: ChatRequest):
    history = get_history(req.session_id)

    history_str = "\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in history[-6:]
    )

    try:
        booking_info = extract_booking_info(req.message)
    except Exception:
        booking_info = {"is_booking": False}

    if booking_info.get("is_booking"):
        booking = create_booking(
            name=booking_info["name"],
            email=booking_info["email"],
            interview_date=booking_info["date"],
            interview_time=booking_info["time"],
        )
        if booking.get("status") == "error":
            reply = f"Sorry, I couldn't complete the booking: {booking.get('message', 'unknown error')}"

        else:
            reply = (
                f"Booking confirmed! Here are the details:\n"
                f"Name: {booking['name']}\n"
                f"Email: {booking['email']}\n"
                f"Date: {booking['date']}\n"
                f"Time: {booking['time']}"
            )
    else:
        chunks = search_documents(req.message)
        context = "\n\n".join(chunks) if chunks else "No relevant documents found."
        reply = generate_response(req.message, context, history_str)

    history.append({"role": "user", "content": req.message})
    history.append({"role": "assistant", "content": reply})
    save_history(req.session_id, history)

    return ChatResponse(reply=reply)
