"""
FitBuddy - Gemini Generative AI Client
Handles communication with Google Gemini API models using google-genai SDK,
with graceful error handling, structured prompting, and offline demo fallback.
"""

import os
import time
import random
from typing import List, Dict, Any

# Try modern google-genai SDK first, fallback to google.generativeai
try:
    from google import genai
    from google.genai import types
    HAS_NEW_GENAI = True
except ImportError:
    HAS_NEW_GENAI = False

try:
    import google.generativeai as legacy_genai
    HAS_LEGACY_GENAI = True
except ImportError:
    HAS_LEGACY_GENAI = False


def call_gemini(prompt: str, system_instruction: str, api_key: str, model_name: str = "gemini-3.8-flash", max_retries: int = 3) -> str:
    """
    Executes a prompt against Gemini API using available SDK.
    Includes automatic exponential backoff retries to handle temporary spikes in demand (503 UNAVAILABLE / 429).
    """
    if not api_key or not api_key.strip():
        raise ValueError("Google Gemini API Key is missing. Please enter your API Key in the sidebar.")

    api_key = api_key.strip()
    target_model = "gemini-3.8-flash"

    last_exception = None

    # Preferred: New google-genai SDK
    if HAS_NEW_GENAI:
        try:
            client = genai.Client(api_key=api_key)
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )

            for attempt in range(max_retries + 1):
                try:
                    response = client.models.generate_content(
                        model=target_model,
                        contents=prompt,
                        config=config,
                    )
                    if response and response.text:
                        return response.text
                except Exception as e:
                    last_exception = e
                    err_str = str(e).lower()
                    is_transient = any(k in err_str for k in ["503", "unavailable", "high demand", "429", "resource_exhausted", "quota", "overloaded"])

                    if is_transient and attempt < max_retries:
                        # Exponential backoff with jitter (1.5s, 3.0s, 6.0s)
                        sleep_time = (1.5 * (2 ** attempt)) + random.uniform(0.2, 0.6)
                        time.sleep(sleep_time)
                        continue
                    else:
                        break
        except Exception as e:
            last_exception = e

    # Fallback: legacy google.generativeai SDK
    if HAS_LEGACY_GENAI:
        try:
            legacy_genai.configure(api_key=api_key)
            for attempt in range(max_retries + 1):
                try:
                    model = legacy_genai.GenerativeModel(
                        model_name=target_model,
                        system_instruction=system_instruction
                    )
                    response = model.generate_content(prompt)
                    if response and response.text:
                        return response.text
                except Exception as e:
                    last_exception = e
                    err_str = str(e).lower()
                    if any(k in err_str for k in ["503", "unavailable", "high demand", "429"]) and attempt < max_retries:
                        time.sleep(2.0)
                        continue
                    break
        except Exception as e:
            last_exception = e

    if last_exception:
        raise last_exception

    raise RuntimeError("Unable to generate content from Gemini API.")


def build_workout_prompt(profile: Dict[str, Any], metrics: Dict[str, Any]) -> tuple:
    system_instruction = (
        "You are FitBuddy, an elite Certified Strength and Conditioning Specialist (CSCS) "
        "and Google Cloud Generative AI Fitness Architect. You design scientifically sound, "
        "highly personalized, progressive workout plans tailored strictly to the user's goals, "
        "equipment, timeline, and physical limitations."
    )

    prompt = f"""
Please generate a comprehensive, personalized weekly workout routine based on the following user assessment:

### User Profile:
- **Age:** {profile.get('age')} years old
- **Gender:** {profile.get('gender')}
- **Height & Weight:** {profile.get('height_cm')} cm | {profile.get('weight_kg')} kg (Target: {profile.get('target_weight_kg')} kg)
- **Primary Goal:** {profile.get('goal')}
- **Experience Level:** {profile.get('experience')}
- **Available Equipment:** {profile.get('equipment')}
- **Training Frequency:** {profile.get('days_per_week')} days per week ({profile.get('session_duration_mins')} minutes per session)
- **Physical Limitations / Injuries:** {profile.get('injuries', 'None')}

### Biometric Calculations:
- **Calculated BMI:** {metrics.get('bmi')} ({metrics.get('bmi_category')})
- **BMR:** {metrics.get('bmr')} kcal | **TDEE:** {metrics.get('tdee')} kcal
- **Daily Target Calories:** {metrics.get('target_calories')} kcal ({metrics.get('calorie_mode')})

### Instructions for the Plan:
1. Provide a clear **Weekly Routine Overview** (e.g. Upper/Lower, Push/Pull/Legs, or Full Body split matching the {profile.get('days_per_week')} days).
2. For each active training day:
   - Provide a dynamic 5-minute **Warm-up routine**.
   - Present the main workout in a neat **Markdown Table** with columns: `Exercise | Sets | Reps | Rest | Key Technique & Safety Cue`.
   - Explicitly honor any injuries mentioned: ({profile.get('injuries')}).
   - Provide a 3-minute **Cool-down / Mobility stretch**.
3. Include **Progressive Overload Rules** (when and how to increase resistance or intensity).
4. Keep the formatting visually clean with emojis, bold headers, and structured bullet points.
"""
    return system_instruction, prompt


def build_meal_prompt(profile: Dict[str, Any], metrics: Dict[str, Any]) -> tuple:
    system_instruction = (
        "You are FitBuddy, an elite Registered Sports Dietitian (RD) and Google Cloud Generative AI "
        "Nutrition Architect. You design delicious, sustainable, macro-accurate meal plans tailored "
        "to biometric energy targets, dietary preferences, and allergies."
    )

    macros = metrics.get('macros', {})
    prompt = f"""
Please generate a comprehensive, personalized daily nutrition blueprint and weekly grocery shopping guide:

### User Profile & Biometrics:
- **Goal:** {profile.get('goal')}
- **Dietary Preference:** {profile.get('diet_type')}
- **Allergies / Dislikes:** {profile.get('allergies', 'None')}
- **Daily Calorie Target:** {metrics.get('target_calories')} kcal ({metrics.get('calorie_mode')})
- **Target Protein:** {macros.get('protein_g')}g ({macros.get('protein_pct')}%)
- **Target Carbohydrates:** {macros.get('carbs_g')}g ({macros.get('carbs_pct')}%)
- **Target Healthy Fats:** {macros.get('fat_g')}g ({macros.get('fat_pct')}%)
- **Minimum Daily Hydration Target:** {metrics.get('hydration_l')} Liters

### Instructions for the Blueprint:
1. Provide a **Daily Macro Breakdown Summary** header.
2. Outline **4 distinct meals / snacks**:
   - **Meal 1 (Breakfast)**
   - **Meal 2 (Lunch)**
   - **Meal 3 (Mid-Day / Pre-or-Post Workout Fuel)**
   - **Meal 4 (Dinner)**
   For each meal, detail the exact ingredients, portion sizes, estimated calories, and macro breakdown (P/C/F), plus quick cooking directions.
3. Provide 2-3 **Smart Food Swaps** (e.g. vegetarian swaps or fast prep alternatives).
4. Provide a structured **Smart Weekly Grocery Checklist** categorized by:
   - Lean Proteins
   - Complex Carbohydrates
   - Healthy Fats
   - Fresh Vegetables & Greens
   - Pantry Essentials & Seasonings
5. Include **Hydration & Electrolyte Timing Tips**.
"""
    return system_instruction, prompt


def generate_coach_offline_response(query: str, profile: Dict[str, Any], metrics: Dict[str, Any]) -> str:
    """
    Generates a personalized, science-grounded response when the live Gemini API is unreachable
    or experiencing a temporary 503 high-demand spike.
    """
    q_lower = query.lower()
    macros = metrics.get('macros', {})
    advice_points = []

    if any(k in q_lower for k in ["knee", "squat", "joint", "hurt", "pain", "injur", "back", "sore"]):
        advice_points.append(
            f"**Injury & Joint Protection:** Because you noted *\"{profile.get('injuries', 'joint sensitivity')}\"*, "
            f"modify high-shear exercises. Substitute deep barbell squats with box squats or unilateral Bulgarian split squats, "
            f"focus on a controlled 3-second eccentric tempo, and never train through sharp joint pain."
        )

    if any(k in q_lower for k in ["protein", "snack", "eat", "food", "shake", "meal", "diet", "nutrition", "hungry"]):
        advice_points.append(
            f"**Nutritional Fueling:** Your daily protein target is **{macros.get('protein_g', 150)}g** ({macros.get('protein_pct', 30)}%) "
            f"with **{metrics.get('target_calories')} kcal** overall. Quick high-yield protein snacks include 200g 0% Greek yogurt (20g protein), "
            f"a whey/plant isolate shake with almond milk (25g protein), or 3 hardboiled egg whites with whole avocado."
        )

    if any(k in q_lower for k in ["weight", "fat", "bulk", "cut", "calorie", "deficit", "surplus"]):
        advice_points.append(
            f"**Energy Balance:** Your calculated Total Daily Energy Expenditure (TDEE) is **{metrics.get('tdee')} kcal**, "
            f"calibrated to a target intake of **{metrics.get('target_calories')} kcal** ({metrics.get('calorie_mode')}). "
            f"Track daily intake consistently and weigh in at the same time each morning under identical conditions."
        )

    if any(k in q_lower for k in ["workout", "exercise", "routine", "split", "reps", "sets", "weight"]):
        advice_points.append(
            f"**Training Prescription:** With your {profile.get('days_per_week')}-day cadence and {profile.get('equipment')}, "
            f"keep sessions capped at **{profile.get('session_duration_mins')} minutes**. Focus on compound multi-joint movements (RPE 7-8) "
            f"and apply progressive overload by increasing load by 1.5 - 2.5kg once you hit the top rep bracket across all working sets."
        )

    if not advice_points:
        advice_points.append(
            f"**Training Guidance:** For your goal of *{profile.get('goal')}* with {profile.get('equipment')}, "
            f"structure your workouts around progressive overload, maintaining strict form and keeping sessions within **{profile.get('session_duration_mins')} minutes**."
        )
        advice_points.append(
            f"**Metabolic Alignment:** Target **{metrics.get('target_calories')} kcal** with **{macros.get('protein_g')}g protein**, "
            f"and consume at least **{metrics.get('hydration_l')} Liters** of water spaced evenly throughout the day."
        )

    advice_text = "\n\n".join([f"- {p}" for p in advice_points])

    return (
        f"**FitBuddy AI Coach:**\n\n"
        f"Here is your personalized guidance for *\"{query}\"*:\n\n"
        f"{advice_text}\n\n"
        f"> *Note: Google Gemini servers are experiencing temporary high demand (503). This response was synthesized by FitBuddy's metabolic science engine.*"
    )


def chat_with_coach(messages: List[Dict[str, str]], profile: Dict[str, Any], metrics: Dict[str, Any], api_key: str, model_name: str = "gemini-3.8-flash") -> str:
    """
    Interactive Q&A with FitBuddy AI Coach holding session memory.
    Resilient to transient 503 high demand spikes with retries and offline science fallback.
    """
    system_instruction = (
        f"You are FitBuddy AI Coach, an expert fitness trainer and sports nutritionist powered by Google Gemini. "
        f"The current user profile is: {profile.get('age')}yo {profile.get('gender')}, goal: {profile.get('goal')}, "
        f"equipment: {profile.get('equipment')}, injuries: {profile.get('injuries')}, "
        f"daily target: {metrics.get('target_calories')} kcal, BMI: {metrics.get('bmi')}. "
        f"Answer the user's fitness, exercise form, injury prevention, recipe, and motivation questions concisely, "
        f"warmly, and scientifically. Use bullet points and bolding for readability."
    )

    # Format message history into prompt
    conversation_history = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages[-6:]])
    prompt = f"Session Context:\n{conversation_history}\n\nASSISTANT (FitBuddy):"

    try:
        return call_gemini(prompt, system_instruction, api_key, model_name)
    except Exception as e:
        err_str = str(e).lower()
        if any(k in err_str for k in ["503", "unavailable", "high demand", "429", "resource_exhausted", "quota"]):
            latest_query = messages[-1]['content'] if messages else "general fitness advice"
            return generate_coach_offline_response(latest_query, profile, metrics)
        raise e
