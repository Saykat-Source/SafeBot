
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



from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI
from datetime import datetime
from fastapi.responses import FileResponse

app = FastAPI()  # <-- THIS MUST COME FIRST

async def get_prompt_template():
    return FileResponse("prompt_template.txt")

with open("prompt_template.txt", "r") as f:
    prompt_template = f.read()

def generate_life_coach_prompt(user_id, user_message, user_budgets):
    data = user_budgets.get(user_id, {})
    today = datetime.now().strftime("%A")
    prompt = prompt_template.format(
        meals_budget=data.get("meals_budget", 0),
        meals_spent=data.get("meals_spent", 0),
        travel_budget=data.get("travel_budget", 0),
        travel_spent=data.get("travel_spent", 0),
        clothes_budget=data.get("clothes_budget", 0),
        clothes_spent=data.get("clothes_spent", 0),
        other_budget=data.get("other_budget", 0),
        other_spent=data.get("other_spent", 0),
        day_of_week=today,
        user_message=user_message
    )
    return prompt
# Initialize your database if needed
# from your_db_module import init_db
# init_db()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client setup
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Pydantic model for request body
class ChatRequest(BaseModel):
    message: str

@app.post("/chat/send")
async def chat_send(request: ChatRequest):
    user_id = "demo_user"  # Replace with real user ID if you add authentication
    user_message = request.message
    prompt = generate_life_coach_prompt(user_id, user_message, user_budgets)
    try:
        response_obj = client.chat.completions.create(
            model="gpt-4",  # or "gpt-4o", "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}]
        )
        ai_reply = response_obj.choices[0].message.content
        print("AI response:", ai_reply)  # Debug print
        return {"reply": ai_reply}
    except Exception as e:
        print("Error from OpenAI:", e)
        return {"reply": "Sorry, I couldn't get a response from the AI."}

from fastapi import Request

@app.post("/update_prompt")
async def update_prompt(request: Request):
    data = await request.json()
    new_prompt = data.get("prompt", "")
    with open("prompt_template.txt", "w") as f:
        f.write(new_prompt)
    return {"message": "Prompt updated successfully!"}
