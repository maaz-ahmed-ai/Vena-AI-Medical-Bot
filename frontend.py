# frontend.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI(title="Clinic AI Frontend")

# ⭐ FIX: SERVE STATIC FILES
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

BACKEND_URL = "http://127.0.0.1:8000/chat"
chat_history = []


def format_bot_message(text: str) -> str:
    text = (
        text.replace("- Name:", "<br><b>Name:</b>")
            .replace("- Email:", "<br><b>Email:</b>")
            .replace("- Phone:", "<br><b>Phone:</b>")
            .replace("- Date of Birth:", "<br><b>Date of Birth:</b>")
            .replace("- Reason:", "<br><b>Reason:</b>")
            .replace("- Date:", "<br><b>Date:</b>")
            .replace("- Time:", "<br><b>Time:</b>")
            .replace("- Notes:", "<br><b>Notes:</b>")
    )
    return text.strip()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "messages": chat_history
    })


@app.post("/send")
async def send_message(request: Request):
    data = await request.json()
    message = data.get("message")
    thread_id = data.get("thread_id") or "frontend-session-001"

    chat_history.append({"sender": "user", "text": message})

    try:
        async with httpx.AsyncClient(timeout=40.0) as client:
            backend_response = await client.post(
                BACKEND_URL,
                json={"question": message, "thread_id": thread_id}
            )

        if backend_response.status_code != 200:
            bot_reply = "Sorry, something went wrong with the server."
        else:
            bot_reply = backend_response.json().get("answer", "")

    except Exception as e:
        bot_reply = f"Server error: {str(e)}"

    bot_reply = format_bot_message(bot_reply)
    chat_history.append({"sender": "bot", "text": bot_reply})

    return JSONResponse({
        "answer": bot_reply,
        "thread_id": thread_id
    })
