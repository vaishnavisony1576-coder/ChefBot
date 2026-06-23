# 🍳 ChefBot AI – Intelligent Recipe Planning Agent

## 📌 Overview

ChefBot AI is an intelligent AI agent that generates complete meal plans based on user queries. Unlike a simple chatbot, it can **plan meals, fetch recipe data, and remember user preferences** to provide personalized food recommendations.

---

## 🤖 Agent Capabilities

### 1. Multi-Step Planning & Execution

* Understands user query (e.g., “spicy Indian dinner”)
* Breaks it into:

  * Cuisine
  * Diet
  * Meal type
* Generates structured meal plan:

  * Starter
  * Main Course
  * Dessert
* Ensures logical and complete output

---

### 2. Tool/API Integration

* Uses external APIs:

  * Gemini API → generates recipes & structured plan
  * Pexels API → fetches food images
* Handles API errors with fallback messages
* Formats response for UI display

---

### 3. Memory & Decision Making

* Stores user preferences:

  * Cuisine
  * Diet
  * Taste (spicy, healthy, etc.)
* Saves memory per user (JSON-based storage)
* Uses memory to personalize future responses

---

## ⚙️ How It Works

1. User enters query (e.g., “healthy breakfast”)
2. System processes:

   * Extracts intent using LLM
   * Reads previous memory
3. LLM generates:

   * Structured meal plan
   * Preferences
4. Backend:

   * Updates memory
   * Fetches images
5. Frontend:

   * Displays cards with recipes
   * Shows detailed view on click

---

## 🏗️ System Architecture

Based on the AI Agent model (Perception → Reasoning → Action → Memory) :

```
User Input
   ↓
Frontend (React UI)
   ↓
FastAPI Backend
   ↓
┌───────────────┐
│ PERCEPTION    │ → Understand query
└───────────────┘
         ↓
┌───────────────┐
│ REASONING     │ → Plan meals (LLM)
└───────────────┘
         ↓
┌───────────────┐
│ ACTION        │ → Fetch images (API)
└───────────────┘
         ↓
┌───────────────┐
│ MEMORY        │ → Store preferences
└───────────────┘
         ↓
Frontend Display
```

---

## 🖥️ Frontend Features

* Modern UI with Bootstrap
* Interactive recipe cards
* Click-to-expand modal view
* Status indicators:

  * Planning
  * Ready
  * Error
* Example queries for quick testing
* Memory display (optional)

---

## 📸 Output Screenshots

### 🔹 Home Screen
<img width="958" height="433" alt="image" src="https://github.com/user-attachments/assets/ee89f694-603d-44d4-a02d-15ab68019cf3" />

### 🔹 Recipe Cards
#### Starter
<img width="1097" height="507" alt="Starter" src="https://github.com/user-attachments/assets/d3760d86-084f-4562-a8e4-9a96416f2bd7" />

#### MainCourse
<img width="1101" height="506" alt="Main Course" src="https://github.com/user-attachments/assets/cdef0be4-55a5-4d2b-90a4-5e75ae167f6d" />

#### Dessert
<img width="1098" height="508" alt="Dessert" src="https://github.com/user-attachments/assets/64527258-e399-4b1a-94a5-972b01694e59" />



### 🔹 Modal View

<img width="1102" height="506" alt="Model Page" src="https://github.com/user-attachments/assets/57847a68-9bad-4103-b348-d6a236b89af0" />


---

## 🛠️ Tech Stack

* Frontend: React + Bootstrap
* Backend: FastAPI (Python)
* AI Model: Gemini API
* APIs:

  * Pexels (images)
* Storage: JSON-based memory system

---

## ⚡ Setup Instructions

### 1. Clone Repository

```bash
git clone <[your-repo-link](https://github.com/vaishnavisony1576-coder/ChefBot)>
cd chefbot
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env`:

```
GEMINI_API_KEY=your_api_key
PEXELS_API_KEY=your_api_key
```

Run:

```bash
uvicorn main:app --reload
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🌐 Deployment

* Frontend: Vercel
* Backend: Render

Live URL:
👉https://chef-bot-pi.vercel.app/

---

## 🔌 API Used

* Gemini API → Recipe generation
* Pexels API → Food images

---

## 👩‍💻 Author

Vaishnavi

---

## 🚀 Project Highlights

* Fully functional AI Agent (not just chatbot)
* Memory-based personalization
* Real API integration
* Clean UI with interactive UX
* Error handling & fallback system

---

## 📌 Example Queries

* spicy indian dinner
* healthy breakfast
* veg lunch
* high protein meal

---

## 🎯 Conclusion

ChefBot AI demonstrates the transition from a simple chatbot to a **full AI agent capable of planning, acting, and remembering**, fulfilling all milestone requirements.

---
