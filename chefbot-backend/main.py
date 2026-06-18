from fastapi import FastAPI
from pydantic import BaseModel
from google.genai import Client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

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


# Create client
client = Client(api_key=os.getenv("GEMINI_API_KEY"))

class RecipeRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "ChefBot running 🚀"}

import time
PROMPT = """
You are ChefBot.

Generate 2 to 3 recipes.

STRICT FORMAT:

For each recipe:

<index>) Recipe Name: <big title>

Ingredients:
♦ item
♦ item
♦ item

Steps:
1. step one
2. step two
3. step three

IMPORTANT RULES:
- Use only "-" for bullets
- Keep headings exactly as:
  "Recipe Name"
  "Ingredients"
  "Steps"
"""
@app.post("/generate-recipe")
def chat(request: RecipeRequest):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",   # ✅ working model
            contents=f"{PROMPT}\n\nUser: {request.query}"
        )

        return {
            "recipe": response.text
        }

    except Exception as e:
        print("Error:", e)

        return {
        "reply": str(e)
         }