from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import sqlite3
from app.llm_integration import query_llm
from app.detection import analyze_output
from app.database import log_interaction

DB_PATH = "biasguard_logs.db"
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Dashboard route
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, prompt, response, issues, model FROM logs ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()
    return templates.TemplateResponse("dashboard.html", {"request": request, "logs": logs})

# Chatbot page route
@router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Chatbot message handler
@router.post("/chat/send")
async def chat_send(request: Request, prompt: str = Form(...), model: str = Form(...)):
    response = query_llm(prompt, model)
    issues = analyze_output(response)
    log_interaction(prompt, response, issues, model)
    return JSONResponse({
        "response": response,
        "issues": issues
    })
