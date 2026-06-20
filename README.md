# 🍳 ChefBot - AI Recipe Generator

ChefBot is a full-stack AI-powered web application that generates recipes based on user-provided ingredients. It combines a modern frontend, scalable backend, and generative AI to deliver structured cooking suggestions in real time.

---

## 🚀 Features

- Generate 2–3 recipes from given ingredients  
- Structured output (Recipe Name, Ingredients, Steps)  
- Chat-based interactive UI  
- Real-time AI-powered responses  
- Fully deployed frontend and backend  

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- JavaScript (ES6+)
- Bootstrap
- Fetch API

### Backend
- FastAPI (Python)
- Uvicorn (ASGI Server)
- Pydantic

### AI Integration
- Google Gemini API (`google.genai` SDK)

### Deployment
- Frontend: Vercel - https://chef-bot-pi.vercel.app/
- Backend: Render - https://chefbot-2-li8u.onrender.com

---

## 🧠 System Architecture

The application follows a client-server architecture with AI integration:

User (Browser)  
↓  
Frontend (React UI)  
↓ HTTP Request (POST /generate-recipe)  
Backend (FastAPI Server)  
↓  
Gemini AI API (LLM Processing)  
↓  
Backend (Response Handling)  
↓  
Frontend (UI Rendering)  
↓  
User (Recipe Output)  

---

## 🔄 Workflow

1. User enters ingredients in the chat interface  
2. Frontend sends POST request to backend  
3. Backend receives input and constructs prompt  
4. Backend sends request to Gemini API  
5. Gemini generates recipes  
6. Backend receives response  
7. Frontend displays formatted output  

---

### Output Screenshots

<img width="959" height="476" alt="Screenshot 2026-06-20 152728" src="https://github.com/user-attachments/assets/a63a5d60-28ee-4a16-996a-2d75d261236d" />

<img width="953" height="473" alt="image" src="https://github.com/user-attachments/assets/d1d88461-94e1-431c-a170-72fde99b1121" />

---

### Author 

 Vaishnavi Gungone

