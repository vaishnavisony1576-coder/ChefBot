

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google.genai import Client
import os

# Load env
load_dotenv()

# FastAPI app
app = FastAPI(
    title="ChefBot API",
    description="AI Recipe Generator",
    version="1.0.0"
)

# CORS (for React later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini Client
client = Client(api_key=os.getenv("GEMINI_API_KEY"))

# System Prompt
SYSTEM_PROMPT = """
You are ChefBot, an AI cooking assistant.

You ONLY answer food and recipe-related questions.

You help users with:
- Recipes based on ingredients
- Cooking steps
- Cuisine suggestions
- Diet-based recipes (veg, vegan, etc.)

If a question is unrelated to cooking,
politely refuse.

Format:
1. Recipe Name
2. Ingredients (bullet points)
3. Steps (numbered)
"""

# Request Model
class ChatRequest(BaseModel):
    message: str

# Health check
@app.get("/")
def health():
    return {
        "status": "online",
        "service": "ChefBot API"
    }

# Chat endpoint
@app.post("/generate-recipe")
def chat(request: ChatRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",   # ✅ working model
            contents=f"{SYSTEM_PROMPT}\n\nUser: {request.query}"
        )

        return {
            "reply": response.text
        }

    except Exception as e:
        print("Error:", e)

    return {
        "reply": str(e)
    }