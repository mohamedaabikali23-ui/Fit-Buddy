"""
FitBuddy - Fitness & Health Calculations Engine
Deterministic calculations for BMI, BMR, TDEE, Target Calories, Macros, and Hydration.
"""

def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
    """
    Calculate Body Mass Index (BMI) and health category.
    Formula: weight (kg) / (height (m) ^ 2)
    """
    if height_cm <= 0 or weight_kg <= 0:
        return {"bmi": 0.0, "category": "Unknown", "color": "#94a3b8", "message": "Invalid inputs"}

    height_m = height_cm / 100.0
    bmi = round(weight_kg / (height_m ** 2), 1)

    if bmi < 18.5:
        category = "Underweight"
        color = "#38bdf8"  # Light blue
        message = "Slightly below healthy weight range. Consider lean caloric surplus."
    elif 18.5 <= bmi < 25.0:
        category = "Normal / Healthy"
        color = "#10b981"  # Emerald green
        message = "You are in an optimal healthy weight range. Focus on body composition."
    elif 25.0 <= bmi < 30.0:
        category = "Overweight"
        color = "#f59e0b"  # Amber
        message = "Slightly above recommended weight. A modest caloric deficit is ideal."
    else:
        category = "Obese"
        color = "#ef4444"  # Rose red
        message = "Higher health risk zone. Gradual, sustainable fat loss is recommended."

    return {
        "bmi": bmi,
        "category": category,
        "color": color,
        "message": message
    }


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> int:
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation.
    Men: (10 × weight) + (6.25 × height) - (5 × age) + 5
    Women: (10 × weight) + (6.25 × height) - (5 × age) - 161
    """
    base = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age)
    if gender.lower() == "male":
        bmr = base + 5
    else:
        bmr = base - 161
    return max(int(round(bmr)), 800)


def calculate_tdee(bmr: int, activity_level: str) -> int:
    """
    Calculate Total Daily Energy Expenditure (TDEE) based on physical activity multipliers.
    """
    multipliers = {
        "Sedentary (desk job, little to no exercise)": 1.2,
        "Lightly Active (1-3 days exercise/week)": 1.375,
        "Moderately Active (3-5 days exercise/week)": 1.55,
        "Very Active (6-7 days hard exercise/week)": 1.725,
        "Extremely Active (athlete / physical labor job)": 1.9
    }
    multiplier = multipliers.get(activity_level, 1.375)
    return int(round(bmr * multiplier))


def calculate_target_calories(tdee: int, goal: str) -> dict:
    """
    Calculate recommended daily caloric target based on user fitness goal.
    """
    goal_lower = goal.lower()
    if "fat loss" in goal_lower or "weight loss" in goal_lower:
        deficit = 450
        target = max(tdee - deficit, 1200)
        mode = "Caloric Deficit (-450 kcal)"
    elif "muscle gain" in goal_lower or "hypertrophy" in goal_lower or "bulk" in goal_lower:
        surplus = 350
        target = tdee + surplus
        mode = "Caloric Surplus (+350 kcal)"
    elif "endurance" in goal_lower:
        surplus = 150
        target = tdee + surplus
        mode = "Performance Fueling (+150 kcal)"
    else:
        target = tdee
        mode = "Maintenance Calories"

    return {
        "target_calories": target,
        "mode": mode,
        "delta": target - tdee
    }


def calculate_macros(target_calories: int, weight_kg: float, goal: str) -> dict:
    """
    Calculate optimal macronutrient split (Protein, Carbs, Fats).
    Protein: 4 kcal/g, Carbs: 4 kcal/g, Fat: 9 kcal/g
    """
    goal_lower = goal.lower()

    if "fat loss" in goal_lower or "weight loss" in goal_lower:
        # High protein to preserve muscle during deficit (2.0g/kg)
        protein_g = min(int(weight_kg * 2.0), int(target_calories * 0.40 / 4))
        fat_cals = target_calories * 0.25
        fat_g = int(fat_cals / 9)
        carb_cals = max(target_calories - (protein_g * 4 + fat_g * 9), 0)
        carbs_g = int(carb_cals / 4)
    elif "muscle gain" in goal_lower or "bulk" in goal_lower:
        # High protein + high carbs for glycogen storage (1.8g/kg)
        protein_g = int(weight_kg * 1.8)
        fat_cals = target_calories * 0.25
        fat_g = int(fat_cals / 9)
        carb_cals = max(target_calories - (protein_g * 4 + fat_g * 9), 0)
        carbs_g = int(carb_cals / 4)
    else:
        # Balanced maintenance / endurance
        protein_g = int(weight_kg * 1.6)
        fat_cals = target_calories * 0.28
        fat_g = int(fat_cals / 9)
        carb_cals = max(target_calories - (protein_g * 4 + fat_g * 9), 0)
        carbs_g = int(carb_cals / 4)

    # Calculate actual calories and percentages
    p_cals = protein_g * 4
    c_cals = carbs_g * 4
    f_cals = fat_g * 9
    total_calculated_cals = p_cals + c_cals + f_cals

    if total_calculated_cals > 0:
        p_pct = int(round((p_cals / total_calculated_cals) * 100))
        c_pct = int(round((c_cals / total_calculated_cals) * 100))
        f_pct = max(100 - (p_pct + c_pct), 0)
    else:
        p_pct, c_pct, f_pct = 30, 45, 25

    return {
        "protein_g": protein_g,
        "carbs_g": carbs_g,
        "fat_g": fat_g,
        "protein_pct": p_pct,
        "carbs_pct": c_pct,
        "fat_pct": f_pct
    }


def calculate_hydration(weight_kg: float, workout_mins_per_day: int) -> float:
    """
    Calculate minimum daily water intake in Liters.
    Baseline: ~35ml per kg + extra 350ml per 30 mins exercise.
    """
    baseline_ml = weight_kg * 35.0
    exercise_ml = (workout_mins_per_day / 30.0) * 350.0
    total_liters = (baseline_ml + exercise_ml) / 1000.0
    return round(total_liters, 1)


def get_ideal_weight_range(height_cm: float) -> tuple:
    """
    Returns ideal healthy weight range (kg) based on BMI 18.5 - 24.9.
    """
    height_m = height_cm / 100.0
    min_w = round(18.5 * (height_m ** 2), 1)
    max_w = round(24.9 * (height_m ** 2), 1)
    return (min_w, max_w)
