"""
FitBuddy - Presets and Sample Data
Provides ready-to-test fitness personas and rich fallback demonstration content.
"""

PRESETS = {
    "Fat Loss & Conditioning": {
        "age": 28,
        "gender": "Male",
        "height_cm": 178,
        "weight_kg": 85.0,
        "target_weight_kg": 75.0,
        "activity_level": "Moderately Active (3-5 days exercise/week)",
        "goal": "Fat Loss / Caloric Deficit",
        "experience": "Intermediate",
        "equipment": "Full Gym Access",
        "days_per_week": 4,
        "session_duration_mins": 45,
        "diet_type": "High Protein Omnivore",
        "allergies": "None",
        "injuries": "Minor knee stiffness on deep squats"
    },
    "Muscle Hypertrophy": {
        "age": 24,
        "gender": "Male",
        "height_cm": 182,
        "weight_kg": 72.0,
        "target_weight_kg": 80.0,
        "activity_level": "Moderately Active (3-5 days exercise/week)",
        "goal": "Muscle Gain / Hypertrophy",
        "experience": "Intermediate",
        "equipment": "Full Gym Access",
        "days_per_week": 5,
        "session_duration_mins": 60,
        "diet_type": "Clean Bulking (High Carb & Protein)",
        "allergies": "None",
        "injuries": "None"
    },
    "Home Workout & Core Tone": {
        "age": 31,
        "gender": "Female",
        "height_cm": 165,
        "weight_kg": 64.0,
        "target_weight_kg": 58.0,
        "activity_level": "Lightly Active (1-3 days exercise/week)",
        "goal": "Fat Loss / Toning",
        "experience": "Beginner",
        "equipment": "Bodyweight & Resistance Bands",
        "days_per_week": 3,
        "session_duration_mins": 30,
        "diet_type": "Vegetarian",
        "allergies": "Gluten Sensitive",
        "injuries": "Lower back fatigue from sitting"
    },
    "Endurance & Running": {
        "age": 35,
        "gender": "Female",
        "height_cm": 170,
        "weight_kg": 60.0,
        "target_weight_kg": 60.0,
        "activity_level": "Very Active (6-7 days hard exercise/week)",
        "goal": "Cardiovascular Endurance",
        "experience": "Advanced",
        "equipment": "Dumbbells & Outdoor / Treadmill",
        "days_per_week": 5,
        "session_duration_mins": 50,
        "diet_type": "Balanced Whole Foods",
        "allergies": "Lactose Intolerant",
        "injuries": "None"
    }
}

SAMPLE_WORKOUT_PLAN = """### 🏋️ Personalized Weekly Training Split: Upper / Lower Hypertrophy & Fat Loss

> **Primary Objective:** Preserve lean muscle mass while accelerating metabolic caloric expenditure.  
> **Cadence:** 4 Days/Week • 45-50 min/session • Moderate-High Intensity (RPE 7-8)

---

#### 📅 Day 1: Upper Body Strength & Density (Chest, Back, Arms)
* **Warm-up (6 mins):** 2 mins light rower/jumping jacks + Arm circles, Band pull-aparts, World's Greatest Stretch.
* **Main Circuit:**

| Exercise | Sets | Reps | Rest | Form Cue / Focus |
| :--- | :---: | :---: | :---: | :--- |
| **Dumbbell Incline Bench Press** | 3 | 8 - 10 | 90s | Retract scapulae, 3-sec controlled lowering |
| **Chest-Supported Chest Row** | 3 | 10 - 12 | 75s | Squeeze rhomboids at top, avoid swinging |
| **Seated Dumbbell Overhead Press** | 3 | 10 - 12 | 75s | Brace core, press vertically without arching back |
| **Lat Pulldown (Neutral Grip)** | 3 | 10 - 12 | 60s | Drive elbows down toward back pockets |
| **Incline Dumbbell Bicep Curls** | 2 | 12 - 15 | 45s | Full elbow extension, eliminate shoulder momentum |
| **Overhead Cable Tricep Extension** | 2 | 12 - 15 | 45s | Keep elbows pinned close to temples |

* **Cool-down (4 mins):** Doorway chest stretch + Lat hanging stretch (60s each).

---

#### 📅 Day 2: Lower Body Power & Knee-Friendly Quads/Glutes
* **Warm-up (6 mins):** Glute bridges, 90/90 hip mobility, bodyweight box squats.
* **Main Circuit:**

| Exercise | Sets | Reps | Rest | Form Cue / Focus |
| :--- | :---: | :---: | :---: | :--- |
| **Romanian Deadlift (Dumbbell or Barbell)** | 3 | 8 - 10 | 90s | Hinge at hips, keep bar glued to thighs |
| **Supported Goblet Box Squat** | 3 | 10 - 12 | 90s | Sit back softly to box to protect knee joints |
| **Bulgarian Split Squat or Walking Lunges** | 3 | 10/leg | 60s | Slight forward torso lean to load glutes |
| **Lying Hamstring Leg Curl** | 3 | 12 - 15 | 60s | Slow eccentric tempo, squeeze at peak |
| **Standing Calf Raises** | 3 | 15 - 20 | 45s | 2-second pause at maximum stretch |
| **Hanging Knee Raises / Planks** | 3 | 12 - 15 | 45s | Tuck pelvis, squeeze abs throughout |

* **Cool-down (4 mins):** Kneeling hip flexor stretch + Pigeon pose.

---

#### 📅 Day 3: Active Recovery & Mobility
* **Recommendation:** 30-40 min brisk outdoor walk (Zone 2 cardio) + full-body foam rolling and dynamic mobility drills. Aim for 8,000 - 10,000 daily steps.

---

#### 📅 Day 4: Upper Body Dynamic Volume & Core
* **Warm-up (5 mins):** Cat-Cow, Scapular push-ups, Deadbugs.
* **Main Circuit:**

| Exercise | Sets | Reps | Rest | Form Cue / Focus |
| :--- | :---: | :---: | :---: | :--- |
| **Flat Dumbbell Press / Push-Ups** | 3 | 10 - 12 | 75s | Tuck elbows at 45-degree angle |
| **Single-Arm Dumbbell Rows** | 3 | 10/side | 60s | Pull dumbbell toward hip crease |
| **Standing Dumbbell Lateral Raises** | 4 | 12 - 15 | 45s | Lead with elbows, thumbs slightly downward |
| **Cable Face Pulls** | 3 | 15 | 45s | Essential for shoulder health and posture |
| **Hammer Curls SS w/ Dips** | 2 | 12 each | 60s | Superset: Arm pump and grip strength |
| **Ab Wheel Rollout or Plank Walkouts**| 3 | 8 - 10 | 60s | Maintain hollow-body position |

---

#### 📅 Day 5: Posterior Chain & Conditioning Finisher
* **Warm-up (5 mins):** Leg swings, Inchworms, Mountain climbers.
* **Main Circuit:**

| Exercise | Sets | Reps | Rest | Form Cue / Focus |
| :--- | :---: | :---: | :---: | :--- |
| **Trap Bar Deadlift or Kettlebell Swings** | 3 | 8 - 10 | 90s | Explosive hip extension, neutral spine |
| **Leg Press (Feet High & Wide)** | 3 | 12 - 15 | 75s | Protects patella while isolating glutes/quads |
| **Seated Leg Extensions (Light/Controlled)**| 2 | 15 - 20 | 45s | Controlled cadence, no jerky motions |
| **HIIT Incline Treadmill or Rower Sprints**| 6 | 30s ON / 30s OFF | - | Maximal effort cardio conditioning |

---

#### 💡 Coach's Progressive Overload Rules:
1. When you can comfortably hit the top rep target on all sets with pristine form, increase weight by 1.5kg - 2.5kg.
2. Prioritize quality of repetition over weight on the bar; never compromise joint safety.
"""

SAMPLE_MEAL_PLAN = """### 🥗 Personalized Nutrition & Macro Blueprint

> **Target Daily Calories:** ~2,100 kcal  
> **Macronutrient Split:**  
> 🥩 **Protein:** 170g (32%) • 🍚 **Carbohydrates:** 210g (40%) • 🥑 **Healthy Fats:** 65g (28%)  
> 💧 **Water Target:** 3.2 Liters / Day

---

#### 🍳 Meal 1: Metabolism Kickstart Breakfast (approx. 520 kcal)
* **Main:** 3 whole scrambled eggs + 1/2 cup egg whites with baby spinach and diced tomatoes.
* **Carbs:** 2 slices of sprouted whole grain toast with 1/4 sliced avocado.
* **Beverage:** Black coffee or green tea + 500ml water with a pinch of pink salt & lemon.
* *Macros:* 38g Protein • 34g Carbs • 22g Fat

---

#### 🥗 Meal 2: Lean Power Lunch (approx. 580 kcal)
* **Main:** 180g grilled herb chicken breast or seared salmon fillet.
* **Carbs:** 1 cup cooked quinoa or fragrant brown basmati rice.
* **Fiber:** 1.5 cups steamed broccoli florets and roasted asparagus with 1 tsp extra virgin olive oil.
* *Macros:* 48g Protein • 52g Carbs • 16g Fat

---

#### ⚡ Meal 3: Pre/Post Workout Fuel (approx. 320 kcal)
* **Shake:** 1 scoop Whey Isolate or Pea Protein + 1 small banana + 1 tbsp chia seeds blended with unsweetened almond milk.
* **Snack:** 1 small handful of raw almonds (15g).
* *Macros:* 30g Protein • 32g Carbs • 8g Fat

---

#### 🍲 Meal 4: Sustained Recovery Dinner (approx. 540 kcal)
* **Main:** 180g lean minced beef (93/7) or seasoned firm tofu stir-fry.
* **Carbs:** 200g roasted sweet potato wedges seasoned with paprika and rosemary.
* **Greens:** Large mixed green salad (kale, arugula, cucumber) with balsamic vinegar and 1 tsp olive oil.
* *Macros:* 42g Protein • 46g Carbs • 16g Fat

---

#### 🛒 Smart Weekly Grocery Checklist:
* **Proteins:** Boneless chicken breasts, lean ground beef/turkey, eggs & egg whites, Greek yogurt (0%), Whey/Plant protein powder.
* **Carbohydrates & Whole Grains:** Quinoa, sweet potatoes, rolled oats, sprouted grain bread, bananas, mixed berries.
* **Healthy Fats:** Avocados, raw almonds, extra virgin olive oil, chia seeds.
* **Vegetables & Greens:** Spinach, arugula, broccoli, asparagus, zucchini, bell peppers.
"""
