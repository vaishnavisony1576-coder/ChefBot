from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from tool import fetch_image
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import json

# 🔥 Load environment variables
load_dotenv()

# 🔥 Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://chef-bot-pi.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEMORY_DIR = "memory"

# create folder if not exists
if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)

def load_memory(user_id):
    filename = os.path.join(MEMORY_DIR, f"memory_{user_id}.json")

    if not os.path.exists(filename):
        return {
            "cuisine": None,
            "diet": None,
            "meal_type": None,
            "preferences": []
        }

    with open(filename, "r") as f:
        return json.load(f)

def save_memory(user_id, memory):
    filename = os.path.join(MEMORY_DIR, f"memory_{user_id}.json")

    with open(filename, "w") as f:
        json.dump(memory, f, indent=4)

class RecipeRequest(BaseModel):
    query: str
    user_id: str


@app.get("/")
def home():
    return {"message": "ChefBot running 🚀"}


# PROMPT (JSON BASED)
PROMPT = """
You are ChefBot AI.

STRICT RULE:
- Only answer food-related queries (recipes, meals, cuisine, diet, ingredients)
- If user asks anything NOT related to food, cooking, recipes:
    Return ONLY this JSON:
    {
    "error": "I am ChefBot. I can only answer food-related queries."
    }
    Do NOT generate any recipes in that case.

--------------------------------

If the query IS food-related:
Generate a complete meal plan.

Return ONLY JSON:

{
  "diet": "veg or non veg",
  "cuisine": "indian/american/etc",
  "meal_type": "breakfast/lunch/dinner",
  "preferences": [],
  "plan": {
    "starter": [
      {
        "name": "",
        "ingredients": [],
        "steps": []
      }
    ],
    "main": [
      {
        "name": "",
        "ingredients": [],
        "steps": []
      }
    ],
    "dessert": [
      {
        "name": "",
        "ingredients": [],
        "steps": []
      }
    ]
  }
}



Rules:
- Extract meal_type from user query. If not mentioned → assume dinner
- Generate exactly 3 dishes in each category
- If meal_type is breakfast:
  starter = []
  dessert = []
  main should contain breakfast items only
- Ingredients must be realistic
- Steps must be clear and short
- Match cuisine properly
- Extract taste preferences (like spicy, sweet, healthy, high protein, etc) from the user query. Always include them in "preferences" if found
- Return ONLY JSON
"""



@app.post("/agent")
def chat(request: RecipeRequest):
    try:
        memory = load_memory(request.user_id)
        context = f"""
        Previous memory:
        {json.dumps(memory)}
        Use this to understand user preferences.
        """
        
        # 🔥 LLM CALL
        try:
            response = model.generate_content(
                f"{context}\n\n{PROMPT}\n\nUser: {request.query}"
            )
            text = response.text.strip()
        except Exception as e:
            print("Gemini Error:", e)
            return {
                "error": "⚠️ Please try again later"
            }
            
        # 🔥 CLEAN RESPONSE (IMPORTANT)
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        # 🔥 CONVERT TO JSON
        try:
            result = json.loads(text)
            if "error" in result:
                return result
        except:
            print("⚠️ Invalid JSON from LLM")

            result = {
                "diet": "veg",
                "cuisine": "indian",
                "meal_type": "dinner",
                "preferences": [],
                "new_preferences": [],
                "plan": {
                    "starter": [],
                    "main": [],
                    "dessert": []
                }
            }
                
        if result.get("cuisine"):
            memory["cuisine"] = result["cuisine"]

        if result.get("diet"):
            memory["diet"] = result["diet"]

        if result.get("meal_type"):
            memory["meal_type"] = result["meal_type"]
        
        if "preferences" not in memory or not isinstance(memory["preferences"], list):
            memory["preferences"] = []
            
        new_prefs = result.get("new_preferences", [])

        # ensure new_prefs is list
        if not isinstance(new_prefs, list):
            new_prefs = []

        # append without duplicates (preserve order)
        for pref in new_prefs:
            if pref not in memory["preferences"]:
                memory["preferences"].append(pref)
                
        print("NEW PREFS:", new_prefs)
        print("UPDATED MEMORY:", memory)
        save_memory(request.user_id, memory)
        
        meal_type = result.get("meal_type", "").lower()
        if meal_type == "breakfast":
            result["plan"]["starter"] = []
            result["plan"]["dessert"] = []
            
        plan = result.get("plan", {})
        if not isinstance(plan, dict):
            plan = {"starter": [], "main": [], "dessert": []}
            
        for category in ["starter", "main", "dessert"]:
            dishes = plan.get(category, [])
            
            for dish in dishes:
                dish["image"] = fetch_image(dish.get("name", "")) or "https://via.placeholder.com/300"
                
        print(result)
        return {
            "structured_output": result,}
        
    except Exception as e:
        print("ERROR:", e)
        return {
            "error": "⚠️ Please try again later"
        }