# 📡 FitBuddy: REST API Specification

This document provides the complete API reference for all endpoints exposed by the **FitBuddy** FastAPI server.

Base URL: `http://127.0.0.1:8000`

---

## 1. Summary of Endpoints

| Method | Endpoint | Description | Consumes | Produces |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Web dashboard root | None | `text/html` |
| `POST` | `/api/profile` | Update biometrics & recalculate metrics | `multipart/form-data` | `application/json` |
| `POST` | `/api/preset/{preset_name}` | Apply persona preset profile | None | `application/json` |
| `POST` | `/api/workout/generate` | Generate AI workout split | `application/json` | `application/json` |
| `POST` | `/api/meal/generate` | Generate AI meal blueprint | `application/json` | `application/json` |
| `POST` | `/api/chat` | AI Coach conversational query | `application/json` | `application/json` |
| `GET` | `/api/export` | Download full regimen dossier | None | `text/markdown` |
| `GET` | `/empathy-map` | Render Empathy Map canvas | None | `text/html` |

---

## 2. Detailed Endpoint Documentation

### `POST /api/profile`
Updates athlete biometrics and deterministically computes new metabolic metrics in SQLite.

#### Form Parameters:
* `age` (*int*, required): Age between 14 and 95.
* `gender` (*string*, required): 'Male' or 'Female'.
* `height_cm` (*float*, required): Stature in cm (120 - 230).
* `weight_kg` (*float*, required): Current weight in kg (35 - 250).
* `target_weight_kg` (*float*, required): Goal weight in kg.
* `goal` (*string*, required): E.g., 'Fat Loss / Caloric Deficit'.
* `activity_level` (*string*, required): Activity multiplier description.
* `experience` (*string*, required): Beginner, Intermediate, Advanced.
* `equipment` (*string*, required): Gym access or equipment type.
* `days_per_week` (*int*, required): 2 to 6 days.
* `session_duration_mins` (*int*, required): 20 to 90 minutes.
* `diet_type` (*string*, required): E.g., 'High Protein Omnivore'.
* `injuries` (*string*, optional): Physical constraints or joint sensitivities.
* `allergies` (*string*, optional): Food dislikes or allergens.

#### Response Example:
```json
{
  "success": true,
  "metrics": {
    "bmi": 26.8,
    "bmi_category": "Overweight",
    "bmr": 1820,
    "tdee": 2821,
    "target_calories": 2371,
    "calorie_mode": "Caloric Deficit (-450 kcal)",
    "hydration_l": 3.5,
    "macros": {
      "protein_g": 170,
      "protein_pct": 29,
      "carbs_g": 242,
      "carbs_pct": 41,
      "fat_g": 66,
      "fat_pct": 30
    }
  }
}
```

---

### `POST /api/preset/{preset_name}`
Loads an athlete persona from the presets collection and recalculates all metrics.

#### Path Parameters:
* `preset_name` (*string*, required): One of:
  * `Fat Loss & Conditioning`
  * `Muscle Hypertrophy`
  * `Home Workout & Core Tone`
  * `Endurance & Running`

---

### `POST /api/workout/generate`
Generates a structured weekly training routine matching user equipment, cadence, and injuries.

#### Request Body (`application/json`):
```json
{
  "api_key": "YOUR_GEMINI_API_KEY",
  "is_demo": false
}
```

#### Response Example:
```json
{
  "success": true,
  "content": "### 🏋️ Personalized Weekly Training Split...\n| Exercise | Sets | Reps | Rest | Cue |...",
  "message": "AI Workout plan generated successfully with Gemini 3.8 Flash!"
}
```

---

### `POST /api/meal/generate`
Generates a 4-tier daily nutrition blueprint and weekly grocery shopping guide.

#### Request Body (`application/json`):
```json
{
  "api_key": "YOUR_GEMINI_API_KEY",
  "is_demo": false
}
```

#### Response Example:
```json
{
  "success": true,
  "content": "### 🥗 Precision Nutrition Blueprint...\n**Meal 1 (Breakfast):**...",
  "message": "AI Nutrition plan generated successfully with Gemini 3.8 Flash!"
}
```

---

### `POST /api/chat`
Sends a question to the session-aware FitBuddy AI Coach.

#### Request Body (`application/json`):
```json
{
  "query": "How do I modify barbell squats to protect my knees?",
  "api_key": "YOUR_GEMINI_API_KEY"
}
```

#### Response Example:
```json
{
  "success": true,
  "answer": "**Coach FitBuddy:** Because of your knee stiffness, replace deep barbell back squats with box squats..."
}
```

---

### `GET /api/export`
Generates and streams an athlete regimen dossier in Markdown format.

#### Response Headers:
* `Content-Type`: `text/markdown`
* `Content-Disposition`: `attachment; filename="FitBuddy_Regimen_Dossier.md"`
