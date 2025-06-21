from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.dashboard import router as dashboard_router
from app.database import init_db

# Initialize the database and create the logs table if it doesn't exist
init_db()

app = FastAPI()
app.include_router(dashboard_router)

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve the chatbot UI at the root URL
@app.get("/", response_class=HTMLResponse)
async def serve_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
