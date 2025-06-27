from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
import csv
from openai import OpenAI
from datetime import datetime
from fastapi import Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi import Depends

# --- Prompt Template ---
TEMPLATE_PATH = "prompt_template.txt"
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    prompt_template = f.read()
print("DEBUG: Loaded prompt template:\n", prompt_template)  # Confirm template is loaded

# --- Example User Data ---
user_budgets = {
    "demo_user": {
        "meals_budget": 100,
        "meals_spent": 60,
        "travel_budget": 50,
        "travel_spent": 40,
        "clothes_budget": 30,
        "clothes_spent": 10,
        "other_budget": 20,
        "other_spent": 5
    }
}

user_profiles = {
    "demo_user": {
        "name": "Alex",
        "age": 27,
        "goals": "Save for a house",
        "preferences": "Healthy food, public transport"
    }
}

recent_activities = {
    "demo_user": "Last week, Alex overspent on travel. Saved $20 on meals."
}

# --- FastAPI App Setup ---
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")
templates = Jinja2Templates(directory="templates")

users = {
    "alice": {"password": "alicepass", "role": "engineer"},
    "bob": {"password": "bobpass", "role": "tester"},
    "admin": {"password": "adminpass", "role": "admin"}
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- OpenAI Client ---
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- Utility Functions ---
def is_prompt_unbiased_keyword(prompt):
    flagged_words = [
        "only for men", "only for women", "rich people", "poor people",
        "lazy", "stupid", "crazy", "normal people"
    ]
    prompt_lower = prompt.lower()
    print("DEBUG: Prompt being checked:", prompt_lower)
    for word in flagged_words:
        print("DEBUG: Checking for:", word)
        if word in prompt_lower:
            print("DEBUG: Flagged phrase detected:", word)
            return False, f"Flagged phrase detected: '{word}'"
    return True, ""

def is_prompt_unbiased_ai(prompt, openai_client):
    review_prompt = (
        "You are an expert in ethical AI. Review the following system prompt for bias, stereotypes, or exclusionary language. "
        "List any issues you find, or say 'No bias detected.'\n\n"
        f"Prompt:\n{prompt}"
    )
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": review_prompt}]
    )
    review = response.choices[0].message.content
    if "No bias detected" in review:
        return True, ""
    else:
        return False, review

def log_prompt(prompt, status, reason="", user_id="unknown"):
    with open("prompt_logs.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            datetime.now().isoformat(),
            user_id,
            status,
            reason,
            prompt.replace('\n', '\\n')
        ])

def generate_life_coach_prompt(
    user_id,
    user_message,
    user_budgets,
    user_profile,
    recent_activity
):
    meals_budget = user_budgets.get("meals_budget", 0)
    meals_spent = user_budgets.get("meals_spent", 0)
    travel_budget = user_budgets.get("travel_budget", 0)
    travel_spent = user_budgets.get("travel_spent", 0)
    clothes_budget = user_budgets.get("clothes_budget", 0)
    clothes_spent = user_budgets.get("clothes_spent", 0)
    other_budget = user_budgets.get("other_budget", 0)
    other_spent = user_budgets.get("other_spent", 0)

    prompt = prompt_template.format(
        bot_name="Finny",
        user_name=user_profile.get("name", "friend"),
        user_age=user_profile.get("age", "unknown"),
        user_goals=user_profile.get("goals", "not set"),
        user_preferences=user_profile.get("preferences", "not set"),
        meals_budget=meals_budget,
        meals_spent=meals_spent,
        travel_budget=travel_budget,
        travel_spent=travel_spent,
        clothes_budget=clothes_budget,
        clothes_spent=clothes_spent,
        other_budget=other_budget,
        other_spent=other_spent,
        meals_budget_minus_spent=meals_budget - meals_spent,
        recent_activity=recent_activity or "No recent activity.",
        day_of_week=datetime.now().strftime("%A"),
        user_message=user_message
    )
    return prompt

# --- Pydantic Model ---
class ChatRequest(BaseModel):
    message: str

# --- Endpoints ---

@app.post("/chat/send")
async def chat_send(request: ChatRequest):
    user_id = "demo_user"  # Replace with real user ID if you add authentication
    user_message = request.message

    # Fetch user data
    user_budget = user_budgets.get(user_id, {})
    user_profile = user_profiles.get(user_id, {})
    recent_activity = recent_activities.get(user_id, "")

    prompt = generate_life_coach_prompt(
        user_id,
        user_message,
        user_budget,
        user_profile,
        recent_activity
    )

    # 1. Keyword-based bias check
    ok, reason = is_prompt_unbiased_keyword(prompt)
    if not ok:
        log_prompt(prompt, "biased (keyword)", reason, user_id)
        return {"reply": f"Sorry, your request could not be processed: {reason}"}

    # 2. AI-powered bias check
    ok, reason = is_prompt_unbiased_ai(prompt, client)
    if not ok:
        log_prompt(prompt, "biased (AI)", reason, user_id)
        return {"reply": f"Sorry, your request could not be processed: {reason}"}

    # 3. If unbiased, log and send to OpenAI for response
    log_prompt(prompt, "unbiased", "", user_id)
    try:
        response_obj = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_reply = response_obj.choices[0].message.content
        print("AI response:", ai_reply)  # Debug print
        return {"reply": ai_reply}
    except Exception as e:
        print("Error from OpenAI:", e)
        return {"reply": "Sorry, I couldn't get a response from the AI."}

@app.get("/prompt_template.txt")
async def get_prompt_template():
    return FileResponse("prompt_template.txt")

@app.post("/update_prompt")
async def update_prompt(request: Request):
    data = await request.json()
    new_prompt = data.get("prompt", "")
    with open("prompt_template.txt", "w") as f:
        f.write(new_prompt)
    return {"message": "Prompt updated successfully!"}

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in users and users[username]["password"] == password:
        request.session["user"] = username
        return RedirectResponse("/welcome", status_code=302)
    # If login fails, show error
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password."})

@app.get("/welcome", response_class=HTMLResponse)
def welcome(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=302)
    return HTMLResponse(f"<h2>Welcome, {user}!</h2>")

@app.get("/submit_prompt", response_class=HTMLResponse)
def submit_prompt_page(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("submit_prompt.html", {"request": request, "user": user})

@app.post("/submit_prompt", response_class=HTMLResponse)
async def submit_prompt(request: Request, prompt: str = Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/", status_code=302)
    # Keyword bias check
    keyword_ok, keyword_reason = is_prompt_unbiased_keyword(prompt)
    # AI bias check (replace 'client' with your OpenAI client variable)
    try:
        ai_ok, ai_reason = is_prompt_unbiased_ai(prompt, client)
    except Exception as e:
        ai_ok, ai_reason = False, f"AI check error: {e}"

    # Log to CSV
    with open("prompt_review_log.csv", "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            datetime.now().isoformat(),
            user,
            prompt.replace('\n', '\\n'),
            "No" if not keyword_ok else "Yes",
            keyword_reason,
            "No" if not ai_ok else "Yes",
            ai_reason
        ])
    # Show result to user
    message = "Prompt submitted! "
    if not keyword_ok:
        message += f"Keyword bias detected: {keyword_reason} "
    if not ai_ok:
        message += f"AI bias detected: {ai_reason}"
    if keyword_ok and ai_ok:
        message += "No bias detected."
    return templates.TemplateResponse("submit_prompt.html", {"request": request, "user": user, "message": message})
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    user = request.session.get("user")
    if not user or users.get(user, {}).get("role") != "admin":
        return RedirectResponse("/", status_code=302)
    logs = []
    try:
        with open("prompt_review_log.csv", "r", encoding="utf-8") as csvfile:
            import csv
            reader = csv.reader(csvfile)
            logs = list(reader)
    except FileNotFoundError:
        pass
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "logs": logs})
