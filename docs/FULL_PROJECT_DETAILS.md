# ⚡ FitBuddy: Full Project Specification & Details

> **Google Cloud Generative AI & Full-Stack Web Application**  
> *Hyper-personalized workout routines, precision metabolic nutrition blueprints, and conversational AI coaching powered by FastAPI, SQLite (SQLAlchemy), Jinja2, and Google Gemini 3.8 Flash.*

---

## 1. Project Overview & Vision
Modern health and fitness guidance is plagued by two extremes: expensive private personal training/clinical dietitians and generic, one-size-fits-all internet workout templates. 

**FitBuddy** bridges this gap by acting as a 24/7 autonomous **AI Fitness & Nutrition Architect**. It uniquely combines:
1. **Deterministic Scientific Precision**: Formulas established by the World Health Organization (WHO) and Mifflin-St Jeor calculate baseline metabolic numbers (BMI, BMR, TDEE, macros, hydration).
2. **Generative AI Customization**: Google's `gemini-3.8-flash` synthesizes these scientific inputs into periodized training routines, 4-tier daily meal blueprints with grocery checklists, and interactive conversational coaching.
3. **Persistent Local Database**: Built on SQLite with SQLAlchemy ORM to save athlete profiles, generated workout and meal routines, and conversational session history.

---

## 2. Core Functional Pillars

### A. Athlete Assessment & Biometric Configuration
* Takes comprehensive physical parameters: Age, Gender, Height, Current Weight, and Goal Target Weight.
* Captures training parameters: Primary Goal, Activity Level, Experience Level, Available Equipment, Weekly Cadence (days/week), and Session Duration.
* Enforces injury and limitation safeguards (e.g., knee stiffness, lower back fatigue).

### B. Deterministic Metabolic Benchmarking
* Computes **Body Mass Index (BMI)** with WHO risk classifications.
* Calculates **Basal Metabolic Rate (BMR)** via Mifflin-St Jeor equations.
* Calculates **Total Daily Energy Expenditure (TDEE)** with activity multipliers.
* Determines exact **Calorie Targets** (Deficit for fat loss, surplus for hypertrophy/endurance).
* Calculates exact gram-level **Macronutrient Targets** (Protein, Carbohydrates, Fats) and hydration goals.

### C. AI-Powered Workout Routine Architecture
* Dynamically formats training splits (Push/Pull/Legs, Upper/Lower, Full Body) matching available equipment and session duration.
* Incorporates 5-minute dynamic warm-ups and 3-minute cool-down mobility stretches.
* Builds structured Markdown tables with exercise names, sets, rep ranges, rest intervals, and technique/injury cues.
* Details progressive overload rules to sustain long-term strength adaptation.

### D. Precision Nutrition & Meal Blueprint
* Constructs 4 balanced meals/snacks: Breakfast, Lunch, Mid-Day Fuel, and Dinner.
* Specifies exact ingredient gram weights, calories, and macronutrient breakdowns (P/C/F).
* Includes smart ingredient swaps for flexible dieting.
* Generates a weekly grocery shopping list categorized into Lean Proteins, Complex Carbs, Healthy Fats, Greens, and Pantry Staples.

### E. Conversational AI Coach
* Session-aware conversational chatbot powered by Gemini 3.8 Flash.
* Pulls chat memory from SQLite to maintain multi-turn context.
* Features one-click prompt starter chips (*Protect Knee Joints*, *Quick Protein Snacks*, *Pre-Workout Fuel*, *Progressive Overload Rules*).
* Features an offline fallback heuristic engine that provides science-grounded answers even during API traffic spikes or when offline.

### F. Dossier Exporter & Audit History
* Compiles the athlete's biometrics, workout split, and meal blueprint into a downloadable Markdown dossier (`FitBuddy_Regimen_Dossier.md`).
* Displays a live history log of saved routines and meal plans fetched directly from `fitbuddy.db`.

---

## 3. Project Directory Map

```text
fitbuddy/
├── docs/                     # Comprehensive documentation suite
│   ├── README.md             # Documentation index
│   ├── FULL_PROJECT_DETAILS.md
│   ├── TECHNICAL_STACK.md
│   ├── ARCHITECTURE_AND_MODELS.md
│   ├── METABOLIC_SCIENCE_ENGINE.md
│   ├── API_REFERENCE.md
│   └── EMPATHY_MAP_AND_PERSONAS.md
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Common layout, styles, scripts, navbar & toast container
│   ├── index.html            # Main 5-tab dashboard interface
│   └── empathy_map.html      # Academic Empathy Map print/view canvas
├── static/                   # Static frontend assets
│   ├── css/
│   │   └── style.css         # Dark glassmorphic design system
│   └── js/
│       └── app.js            # Asynchronous frontend controller (AJAX, tabs, chat)
├── main.py                   # FastAPI application, routes, and API controllers
├── database.py               # SQLite database engine and session dependency
├── models.py                 # SQLAlchemy ORM models (UserProfile, WorkoutPlan, MealPlan, ChatMessage)
├── calculator.py             # Deterministic metabolic calculation engine
├── gemini_client.py          # Google GenAI SDK integration with retry backoff & fallback
├── sample_data.py            # Athlete presets and demo demonstration plans
├── generate_docx.py          # Microsoft Word (.docx) generator for Empathy Map
├── app.py                    # Companion standalone Streamlit application
├── styles.py                 # Custom CSS injector for Streamlit interface
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── fitbuddy.db               # SQLite database file
```

---

## 4. Resilience & Error Handling Architecture

1. **Transient API Error Recovery (503 & 429)**:
   In [`gemini_client.py`](file:///c:/Users/ADMIN/.gemini/antigravity-ide/scratch/fitbuddy/gemini_client.py), calls to Google Gemini are wrapped in exponential backoff retry loops with randomized jitter (`1.5s`, `3.0s`, `6.0s`).
2. **Offline Fallback Engine**:
   If Gemini is unreachable or API keys are not provided, FitBuddy seamlessly switches to its offline heuristic engine ([`generate_coach_offline_response`](file:///c:/Users/ADMIN/.gemini/antigravity-ide/scratch/fitbuddy/gemini_client.py#L182)) or pre-calibrated sample data ([`sample_data.py`](file:///c:/Users/ADMIN/.gemini/antigravity-ide/scratch/fitbuddy/sample_data.py)).
3. **Database Thread-Safety**:
   The SQLite connection in [`database.py`](file:///c:/Users/ADMIN/.gemini/antigravity-ide/scratch/fitbuddy/database.py) uses `check_same_thread=False` to safely handle concurrent ASGI threads in FastAPI.
