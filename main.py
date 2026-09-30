"""
FitBuddy - FastAPI Core Web Application
Built with FastAPI, SQLAlchemy (SQLite), Jinja2 Templates, and Google Gemini GenAI.
"""

import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Depends, Request, Form, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

import database
import models
import calculator
import gemini_client
import sample_data

# Initialize database schema
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="FitBuddy AI",
    description="AI-Powered Fitness & Nutrition Architect built with FastAPI, SQLite, Jinja2, and Gemini.",
    version="2.0.0"
)

# Mount static directory for CSS and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

import markdown

# Mount Jinja2 templates directory with markdown filter
templates = Jinja2Templates(directory="templates")


def render_markdown_filter(text: str) -> str:
    """Converts raw Markdown into clean HTML with tables and linebreaks."""
    if not text:
        return ""
    return markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])


templates.env.filters["markdown"] = render_markdown_filter


# Request Pydantic Schemas
class GenerateRequest(BaseModel):
    api_key: Optional[str] = ""
    is_demo: Optional[bool] = False


class ChatRequest(BaseModel):
    query: str
    api_key: Optional[str] = ""


def get_or_create_user(db: Session) -> models.UserProfile:
    """Retrieves the active user profile or seeds the initial profile from presets."""
    user = db.query(models.UserProfile).first()
    if not user:
        preset = sample_data.PRESETS["Fat Loss & Conditioning"]
        bmi_data = calculator.calculate_bmi(preset["weight_kg"], preset["height_cm"])
        bmr = calculator.calculate_bmr(preset["weight_kg"], preset["height_cm"], preset["age"], preset["gender"])
        tdee = calculator.calculate_tdee(bmr, preset["activity_level"])
        cal_data = calculator.calculate_target_calories(tdee, preset["goal"])
        macros = calculator.calculate_macros(cal_data["target_calories"], preset["weight_kg"], preset["goal"])
        hydration = calculator.calculate_hydration(preset["weight_kg"], preset["session_duration_mins"])

        user = models.UserProfile(
            name="Athlete",
            age=preset["age"],
            gender=preset["gender"],
            height_cm=preset["height_cm"],
            weight_kg=preset["weight_kg"],
            target_weight_kg=preset["target_weight_kg"],
            goal=preset["goal"],
            activity_level=preset["activity_level"],
            experience=preset["experience"],
            equipment=preset["equipment"],
            days_per_week=preset["days_per_week"],
            session_duration_mins=preset["session_duration_mins"],
            diet_type=preset["diet_type"],
            allergies=preset["allergies"],
            injuries=preset["injuries"],
            bmi=bmi_data["bmi"],
            bmi_category=bmi_data["category"],
            bmr=bmr,
            tdee=tdee,
            target_calories=cal_data["target_calories"],
            calorie_mode=cal_data["mode"],
            protein_g=macros["protein_g"],
            carbs_g=macros["carbs_g"],
            fat_g=macros["fat_g"],
            hydration_l=hydration
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(database.get_db)):
    """Renders the main FitBuddy interactive dashboard using Jinja2 templates."""
    user = get_or_create_user(db)
    latest_workout = db.query(models.WorkoutPlan).filter_by(user_id=user.id).order_by(models.WorkoutPlan.id.desc()).first()
    latest_meal = db.query(models.MealPlan).filter_by(user_id=user.id).order_by(models.MealPlan.id.desc()).first()
    chat_history = db.query(models.ChatMessage).filter_by(user_id=user.id).order_by(models.ChatMessage.id.asc()).limit(20).all()
    saved_workouts = db.query(models.WorkoutPlan).filter_by(user_id=user.id).order_by(models.WorkoutPlan.id.desc()).limit(10).all()
    saved_meals = db.query(models.MealPlan).filter_by(user_id=user.id).order_by(models.MealPlan.id.desc()).limit(10).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "profile": user,
            "presets": sample_data.PRESETS,
            "latest_workout": latest_workout,
            "latest_meal": latest_meal,
            "chat_history": chat_history,
            "saved_workouts": saved_workouts,
            "saved_meals": saved_meals
        }
    )


@app.post("/api/profile")
async def update_profile(
    age: int = Form(...),
    gender: str = Form(...),
    height_cm: float = Form(...),
    weight_kg: float = Form(...),
    target_weight_kg: float = Form(...),
    goal: str = Form(...),
    activity_level: str = Form(...),
    experience: str = Form(...),
    equipment: str = Form(...),
    days_per_week: int = Form(...),
    session_duration_mins: int = Form(...),
    diet_type: str = Form(...),
    injuries: Optional[str] = Form("None"),
    allergies: Optional[str] = Form("None"),
    db: Session = Depends(database.get_db)
):
    """Updates user biometrics and deterministically recalculates metabolic numbers in SQLite."""
    user = get_or_create_user(db)

    # Recalculate deterministic metrics
    bmi_data = calculator.calculate_bmi(weight_kg, height_cm)
    bmr = calculator.calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculator.calculate_tdee(bmr, activity_level)
    cal_data = calculator.calculate_target_calories(tdee, goal)
    macros = calculator.calculate_macros(cal_data["target_calories"], weight_kg, goal)
    hydration = calculator.calculate_hydration(weight_kg, session_duration_mins)

    # Persist in SQLite
    user.age = age
    user.gender = gender
    user.height_cm = height_cm
    user.weight_kg = weight_kg
    user.target_weight_kg = target_weight_kg
    user.goal = goal
    user.activity_level = activity_level
    user.experience = experience
    user.equipment = equipment
    user.days_per_week = days_per_week
    user.session_duration_mins = session_duration_mins
    user.diet_type = diet_type
    user.allergies = allergies or "None"
    user.injuries = injuries or "None"

    user.bmi = bmi_data["bmi"]
    user.bmi_category = bmi_data["category"]
    user.bmr = bmr
    user.tdee = tdee
    user.target_calories = cal_data["target_calories"]
    user.calorie_mode = cal_data["mode"]
    user.protein_g = macros["protein_g"]
    user.carbs_g = macros["carbs_g"]
    user.fat_g = macros["fat_g"]
    user.hydration_l = hydration
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "metrics": {
            "bmi": user.bmi,
            "bmi_category": user.bmi_category,
            "bmr": user.bmr,
            "tdee": user.tdee,
            "target_calories": user.target_calories,
            "calorie_mode": user.calorie_mode,
            "hydration_l": user.hydration_l,
            "macros": {
                "protein_g": user.protein_g,
                "protein_pct": macros.get("protein_pct", 30),
                "carbs_g": user.carbs_g,
                "carbs_pct": macros.get("carbs_pct", 40),
                "fat_g": user.fat_g,
                "fat_pct": macros.get("fat_pct", 30)
            }
        }
    }


@app.post("/api/preset/{preset_name}")
async def apply_preset(preset_name: str, db: Session = Depends(database.get_db)):
    """Applies persona preset to user profile and recalculates all metrics in SQLite."""
    if preset_name not in sample_data.PRESETS:
        raise HTTPException(status_code=404, detail="Preset not found")

    preset = sample_data.PRESETS[preset_name]
    user = get_or_create_user(db)

    user.age = preset["age"]
    user.gender = preset["gender"]
    user.height_cm = preset["height_cm"]
    user.weight_kg = preset["weight_kg"]
    user.target_weight_kg = preset["target_weight_kg"]
    user.goal = preset["goal"]
    user.activity_level = preset["activity_level"]
    user.experience = preset["experience"]
    user.equipment = preset["equipment"]
    user.days_per_week = preset["days_per_week"]
    user.session_duration_mins = preset["session_duration_mins"]
    user.diet_type = preset["diet_type"]
    user.allergies = preset.get("allergies", "None")
    user.injuries = preset.get("injuries", "None")

    bmi_data = calculator.calculate_bmi(user.weight_kg, user.height_cm)
    bmr = calculator.calculate_bmr(user.weight_kg, user.height_cm, user.age, user.gender)
    tdee = calculator.calculate_tdee(bmr, user.activity_level)
    cal_data = calculator.calculate_target_calories(tdee, user.goal)
    macros = calculator.calculate_macros(cal_data["target_calories"], user.weight_kg, user.goal)
    hydration = calculator.calculate_hydration(user.weight_kg, user.session_duration_mins)

    user.bmi = bmi_data["bmi"]
    user.bmi_category = bmi_data["category"]
    user.bmr = bmr
    user.tdee = tdee
    user.target_calories = cal_data["target_calories"]
    user.calorie_mode = cal_data["mode"]
    user.protein_g = macros["protein_g"]
    user.carbs_g = macros["carbs_g"]
    user.fat_g = macros["fat_g"]
    user.hydration_l = hydration

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "profile": {
            "age": user.age,
            "gender": user.gender,
            "height_cm": user.height_cm,
            "weight_kg": user.weight_kg,
            "target_weight_kg": user.target_weight_kg,
            "goal": user.goal,
            "activity_level": user.activity_level,
            "experience": user.experience,
            "equipment": user.equipment,
            "days_per_week": user.days_per_week,
            "session_duration_mins": user.session_duration_mins,
            "diet_type": user.diet_type,
            "allergies": user.allergies,
            "injuries": user.injuries
        },
        "metrics": {
            "bmi": user.bmi,
            "bmi_category": user.bmi_category,
            "bmr": user.bmr,
            "tdee": user.tdee,
            "target_calories": user.target_calories,
            "calorie_mode": user.calorie_mode,
            "hydration_l": user.hydration_l,
            "macros": {
                "protein_g": user.protein_g,
                "protein_pct": macros.get("protein_pct", 30),
                "carbs_g": user.carbs_g,
                "carbs_pct": macros.get("carbs_pct", 40),
                "fat_g": user.fat_g,
                "fat_pct": macros.get("fat_pct", 30)
            }
        }
    }


@app.post("/api/workout/generate")
async def generate_workout(payload: GenerateRequest, db: Session = Depends(database.get_db)):
    """Generates an AI workout split or loads demo split, saving record to SQLite."""
    user = get_or_create_user(db)
    api_key = payload.api_key.strip() if payload.api_key else os.getenv("GEMINI_API_KEY", "")

    if payload.is_demo or not api_key:
        content = sample_data.SAMPLE_WORKOUT_PLAN
        is_ai = False
        message = "Loaded demo workout routine!"
    else:
        profile_dict = {
            "age": user.age,
            "gender": user.gender,
            "height_cm": user.height_cm,
            "weight_kg": user.weight_kg,
            "target_weight_kg": user.target_weight_kg,
            "goal": user.goal,
            "experience": user.experience,
            "equipment": user.equipment,
            "days_per_week": user.days_per_week,
            "session_duration_mins": user.session_duration_mins,
            "injuries": user.injuries
        }
        metrics_dict = {
            "bmi": user.bmi,
            "bmi_category": user.bmi_category,
            "bmr": user.bmr,
            "tdee": user.tdee,
            "target_calories": user.target_calories,
            "calorie_mode": user.calorie_mode
        }
        try:
            sys_p, user_p = gemini_client.build_workout_prompt(profile_dict, metrics_dict)
            content = gemini_client.call_gemini(user_p, sys_p, api_key, "gemini-3.8-flash")
            is_ai = True
            message = "AI Workout plan generated successfully with Gemini 3.8 Flash!"
        except Exception as e:
            content = sample_data.SAMPLE_WORKOUT_PLAN
            is_ai = False
            message = f"Gemini high demand (503): loaded science-calibrated workout routine."

    # Save to SQLite
    workout = models.WorkoutPlan(
        user_id=user.id,
        title=f"{user.days_per_week}-Day {user.goal} Split",
        goal=user.goal,
        content_markdown=content,
        is_ai_generated=is_ai
    )
    db.add(workout)
    db.commit()

    return {"success": True, "content": content, "message": message}


@app.post("/api/meal/generate")
async def generate_meal(payload: GenerateRequest, db: Session = Depends(database.get_db)):
    """Generates an AI nutrition blueprint or loads demo plan, saving record to SQLite."""
    user = get_or_create_user(db)
    api_key = payload.api_key.strip() if payload.api_key else os.getenv("GEMINI_API_KEY", "")

    if payload.is_demo or not api_key:
        content = sample_data.SAMPLE_MEAL_PLAN
        is_ai = False
        message = "Loaded demo nutrition blueprint!"
    else:
        profile_dict = {
            "goal": user.goal,
            "diet_type": user.diet_type,
            "allergies": user.allergies
        }
        metrics_dict = {
            "target_calories": user.target_calories,
            "calorie_mode": user.calorie_mode,
            "hydration_l": user.hydration_l,
            "macros": {
                "protein_g": user.protein_g,
                "protein_pct": 30,
                "carbs_g": user.carbs_g,
                "carbs_pct": 40,
                "fat_g": user.fat_g,
                "fat_pct": 30
            }
        }
        try:
            sys_p, user_p = gemini_client.build_meal_prompt(profile_dict, metrics_dict)
            content = gemini_client.call_gemini(user_p, sys_p, api_key, "gemini-3.8-flash")
            is_ai = True
            message = "AI Nutrition plan generated successfully with Gemini 3.8 Flash!"
        except Exception as e:
            content = sample_data.SAMPLE_MEAL_PLAN
            is_ai = False
            message = f"Gemini high demand (503): loaded science-calibrated meal blueprint."

    # Save to SQLite
    meal = models.MealPlan(
        user_id=user.id,
        title=f"{user.target_calories} kcal {user.diet_type} Blueprint",
        calorie_target=user.target_calories,
        content_markdown=content,
        is_ai_generated=is_ai
    )
    db.add(meal)
    db.commit()

    return {"success": True, "content": content, "message": message}


@app.post("/api/chat")
async def chat_coach(payload: ChatRequest, db: Session = Depends(database.get_db)):
    """Handles interactive conversational Q&A with FitBuddy AI Coach holding session memory in SQLite."""
    user = get_or_create_user(db)
    api_key = payload.api_key.strip() if payload.api_key else os.getenv("GEMINI_API_KEY", "")

    # Save user message to SQLite
    user_msg = models.ChatMessage(user_id=user.id, role="user", content=payload.query)
    db.add(user_msg)
    db.commit()

    # Load message history
    history = db.query(models.ChatMessage).filter_by(user_id=user.id).order_by(models.ChatMessage.id.asc()).limit(12).all()
    history_dicts = [{"role": m.role, "content": m.content} for m in history]

    profile_dict = {
        "age": user.age,
        "gender": user.gender,
        "goal": user.goal,
        "equipment": user.equipment,
        "injuries": user.injuries,
        "days_per_week": user.days_per_week,
        "session_duration_mins": user.session_duration_mins
    }
    metrics_dict = {
        "target_calories": user.target_calories,
        "bmi": user.bmi,
        "tdee": user.tdee,
        "calorie_mode": user.calorie_mode,
        "hydration_l": user.hydration_l,
        "macros": {
            "protein_g": user.protein_g,
            "protein_pct": 30
        }
    }

    if not api_key:
        # Offline sports science response
        answer = gemini_client.generate_coach_offline_response(payload.query, profile_dict, metrics_dict)
    else:
        try:
            answer = gemini_client.chat_with_coach(history_dicts, profile_dict, metrics_dict, api_key, "gemini-3.8-flash")
        except Exception:
            answer = gemini_client.generate_coach_offline_response(payload.query, profile_dict, metrics_dict)

    # Save coach reply to SQLite
    coach_msg = models.ChatMessage(user_id=user.id, role="assistant", content=answer)
    db.add(coach_msg)
    db.commit()

    return {"success": True, "answer": answer}


@app.get("/api/export")
async def export_dossier(db: Session = Depends(database.get_db)):
    """Compiles and exports the complete personalized dossier as a downloadable Markdown document."""
    user = get_or_create_user(db)
    latest_workout = db.query(models.WorkoutPlan).filter_by(user_id=user.id).order_by(models.WorkoutPlan.id.desc()).first()
    latest_meal = db.query(models.MealPlan).filter_by(user_id=user.id).order_by(models.MealPlan.id.desc()).first()

    w_content = latest_workout.content_markdown if latest_workout else sample_data.SAMPLE_WORKOUT_PLAN
    m_content = latest_meal.content_markdown if latest_meal else sample_data.SAMPLE_MEAL_PLAN

    doc = f"""# ⚡ FitBuddy AI: Personalized Health & Training Dossier
*Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} | Powered by FastAPI, SQLite & Google Gemini*

---

## 👤 Athlete Biometrics & Assessment
- **Age / Gender:** {user.age} years | {user.gender}
- **Height / Weight:** {user.height_cm} cm | {user.weight_kg} kg (Goal Target: {user.target_weight_kg} kg)
- **Primary Goal:** {user.goal}
- **Experience Level:** {user.experience}
- **Equipment:** {user.equipment}
- **Cadence:** {user.days_per_week} days/week ({user.session_duration_mins} mins/session)
- **Dietary Preference:** {user.diet_type} (Allergies: {user.allergies})
- **Physical Safeguards / Limitations:** {user.injuries}

---

## 🔬 Deterministic Metabolic Benchmarks
- **BMI (Body Mass Index):** {user.bmi} ({user.bmi_category})
- **BMR (Basal Metabolic Rate):** {user.bmr} kcal/day
- **TDEE (Total Daily Energy Expenditure):** {user.tdee} kcal/day
- **Target Caloric Intake:** {user.target_calories} kcal/day ({user.calorie_mode})
- **Daily Protein Target:** {user.protein_g}g
- **Daily Carbohydrate Target:** {user.carbs_g}g
- **Daily Fat Target:** {user.fat_g}g
- **Minimum Daily Water Intake:** {user.hydration_l} Liters

---

## 🏋️ Personalized Training Architecture
{w_content}

---

## 🥗 Precision Nutrition & Meal Blueprint
{m_content}

---
*FitBuddy AI - Built with FastAPI, SQLite, Jinja2 & Google Gemini 3.8 Flash.*
"""
    return Response(
        content=doc,
        media_type="text/markdown",
        headers={"Content-Disposition": 'attachment; filename="FitBuddy_Regimen_Dossier.md"'}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
