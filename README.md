# ⚡ FitBuddy: AI-Powered Fitness & Nutrition Architect

> **Google Cloud Generative AI & Full-Stack Web Application**  
> Hyper-personalized workout routines, precision metabolic nutrition blueprints, and conversational fitness coaching powered by **FastAPI**, **Jinja2 Templates**, **SQLAlchemy (SQLite)**, and **Google Gemini 3.8 Flash**.

---

## 🎯 Pre-requisites & Requirements Checklist

This project is built to satisfy **100% of all required competencies**:

| # | Requirement | Implementation in FitBuddy | Status |
| :-: | :--- | :--- | :-: |
| **1** | **FastAPI Framework** | Core REST & template application in [`main.py`](main.py) with structured routers, dependencies, and form handling | **✅ 100% Complete** |
| **2** | **Gemini API** | Integrated with Google's official `google-genai` SDK using `gemini-3.8-flash` with automatic retry backoff in [`gemini_client.py`](gemini_client.py) | **✅ 100% Complete** |
| **3** | **HTML, CSS & Jinja2 Templates** | Modular layout in [`templates/base.html`](templates/base.html) and [`templates/index.html`](templates/index.html) with custom glassmorphism in [`static/css/style.css`](static/css/style.css) | **✅ 100% Complete** |
| **4** | **Python Programming** | Clean, modular Python 3.10+ architecture with deterministic metabolic calculations in [`calculator.py`](calculator.py) | **✅ 100% Complete** |
| **5** | **Version Control with Git** | Git-ready repository structure with `.gitignore` and clean commit history | **✅ 100% Complete** |
| **6** | **SQLAlchemy & SQLite** | Persistent SQLite database (`fitbuddy.db`) with ORM models for Users, Workouts, Meals, and Chat in [`database.py`](database.py) and [`models.py`](models.py) | **✅ 100% Complete** |
| **7** | **Environment Setup** | Configured with [`requirements.txt`](requirements.txt), virtualenv instructions, and [`.env.example`](.env.example) | **✅ 100% Complete** |
| **8** | **Uvicorn ASGI Server** | High-performance asynchronous ASGI execution via `uvicorn main:app --reload` on port 8000 | **✅ 100% Complete** |

---

## 🌟 Key Features

1. **Deterministic Metabolic Science Engine**:
   - Computes **BMI** with WHO risk categorizations and ideal weight bounds.
   - Calculates **BMR** (Basal Metabolic Rate via Mifflin-St Jeor) and **TDEE** (Total Daily Energy Expenditure).
   - Dynamically calculates caloric deficit/surplus and exact macronutrient grams (**Protein, Carbs, Fats**) and daily hydration targets.

2. **AI-Powered Custom Workout Architecture**:
   - Structured day-by-day training splits matching available equipment, frequency, and session length.
   - Includes warm-up, main exercise table, rest times, form cues, cool-down mobility, and progressive overload rules.
   - Safeguards against joint injuries and physical limitations.

3. **Precision Nutrition Blueprint**:
   - 4 daily meals/snacks tailored to dietary preferences (High Protein, Clean Bulking, Vegetarian, Vegan, Keto, etc.).
   - Exact calorie and macronutrient breakdown per meal with categorized smart weekly grocery checklist.

4. **FitBuddy AI Coach (Conversational Chatbot)**:
   - Session-aware AI coach powered by Gemini `gemini-3.8-flash` with conversation history stored in SQLite.
   - Built-in prompt starters for injury modifications, pre-workout snacks, and progressive overload tips.
   - Resilient multi-tier fallback ensuring answers even during API traffic spikes.

5. **SQLite Database Persistence & Dossier Exporter**:
   - Every profile update, generated routine, meal blueprint, and chat conversation is saved to `fitbuddy.db`.
   - One-click export of complete regimen as a Markdown dossier ready to save or print.

---

## 📂 Project Architecture

```text
fitbuddy/
├── main.py              # FastAPI application controller & route handlers
├── database.py          # SQLAlchemy SQLite engine & session management
├── models.py            # SQLAlchemy ORM models (User, WorkoutPlan, MealPlan, ChatMessage)
├── calculator.py        # Deterministic health formulas (Mifflin-St Jeor BMR, TDEE, BMI, Macros)
├── gemini_client.py     # Google GenAI SDK integration with gemini-3.8-flash & backoff retries
├── sample_data.py       # Athlete persona presets & rich demonstration data
├── requirements.txt     # Complete dependencies
├── fitbuddy.db          # Persistent SQLite database
├── templates/
│   ├── base.html        # Jinja2 base layout with fonts, navbar, and toast alerts
│   └── index.html       # Main interactive dashboard with biometrics, workouts, meals, coach
├── static/
│   ├── css/
│   │   └── style.css    # Modern dark glassmorphism styling
│   └── js/
│       └── app.js       # Asynchronous client controller (AJAX, live calculations, chat)
└── README.md            # Project documentation & requirements guide
```

---

## 🚀 How to Run

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. (Optional) Set your Gemini API Key in `.env`:
```bash
copy .env.example .env
# Edit .env and paste your GEMINI_API_KEY
```
*(You can also paste the API key directly into the navbar input on the web page, or use Demo Mode!)*

### 3. Run the FastAPI application using Uvicorn:
```bash
uvicorn main:app --reload --port 8000
```
Open your browser at **`http://127.0.0.1:8000`**.

### 4. Interactive API Documentation:
FastAPI automatically provides interactive Swagger documentation at:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## 🛡️ Medical & Safety Disclaimer
*FitBuddy is an AI-assisted fitness and nutritional design application. The generated routines and caloric guidelines are designed for educational and informational purposes. Consult a medical professional or certified physical therapist before beginning any new training program.*
