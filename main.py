from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
import os
import csv
import json
from openai import OpenAI
from datetime import datetime

# --- Prompt Template ---
TEMPLATE_PATH = "prompt_template.txt"
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    prompt_template = f.read()
print("DEBUG: Loaded prompt template:\n", prompt_template)

# --- User Data Files ---
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# --- Example User Data (for demo user) ---
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

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str

class PromptCheckRequest(BaseModel):
    prompt: str

# --- API Endpoints ---

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

    try:
        response_obj = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_reply = response_obj.choices[0].message.content
        print("AI response:", ai_reply)  # Debug print

        # 1. Keyword-based bias check on AI reply
        ok_keyword, reason_keyword = is_prompt_unbiased_keyword(ai_reply)
        if not ok_keyword:
            log_prompt(prompt, "biased (keyword)", reason_keyword, user_id)
        # 2. AI-powered bias check on AI reply
        ok_ai, reason_ai = is_prompt_unbiased_ai(ai_reply, client)
        if not ok_ai:
            log_prompt(prompt, "biased (AI)", reason_ai, user_id)
        # 3. If unbiased, log as usual
        if ok_keyword and ok_ai:
            log_prompt(prompt, "unbiased", "", user_id)

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

@app.post("/check_prompt")
async def check_prompt(request: PromptCheckRequest):
    prompt = request.prompt
    # Run your bias checks
    ok_keyword, reason_keyword = is_prompt_unbiased_keyword(prompt)
    ok_ai, reason_ai = is_prompt_unbiased_ai(prompt, client)
    is_biased = not (ok_keyword and ok_ai)
    reason = reason_keyword if not ok_keyword else reason_ai if not ok_ai else ""
    result = "biased" if is_biased else "unbiased"

    # Log the prompt and result (append to a CSV or database)
    with open("prompt_practice_log.csv", "a") as f:
        f.write(f"{datetime.now()},{prompt},{result},{reason}\n")

    return {
        "result": result,
        "reason": reason
    }

# --- Serve React App at Root and All Unmatched Routes ---

# Serve static files (JS, CSS, etc.)
app.mount("/static", StaticFiles(directory="static/react"), name="static")

# Serve React index.html at root
@app.get("/", response_class=HTMLResponse)
async def serve_react():
    return FileResponse("static/react/index.html")

# Serve React for all unmatched routes (so React Router works)
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_react_catchall(full_path: str):
    file_path = os.path.join("static/react", full_path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return FileResponse(file_path)
    return FileResponse("static/react/index.html")
