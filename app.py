"""
FitBuddy - AI Fitness & Nutrition Companion
Powered by Google Cloud Generative AI & Gemini Models
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

from calculator import (
    calculate_bmi,
    calculate_bmr,
    calculate_tdee,
    calculate_target_calories,
    calculate_macros,
    calculate_hydration,
    get_ideal_weight_range
)
from styles import get_custom_css
from sample_data import PRESETS, SAMPLE_WORKOUT_PLAN, SAMPLE_MEAL_PLAN
import importlib
import gemini_client
importlib.reload(gemini_client)

# Streamlit Page Configuration
st.set_page_config(
    page_title="FitBuddy - AI Fitness & Nutrition Companion",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize Session State
if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = None
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hi there! I'm your FitBuddy AI Coach. Feel free to ask me for exercise modifications, pre-workout meals, or recovery tips anytime!"}
    ]
if "active_preset" not in st.session_state:
    st.session_state.active_preset = "Fat Loss & Conditioning"

# --- SIDEBAR: Configuration & Presets ---
with st.sidebar:
    st.markdown("## ⚡ FitBuddy AI")
    st.caption("Google Cloud Generative AI Track")
    st.markdown("---")

    # API Key Handling
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "🔑 Gemini API Key",
        value=env_key,
        type="password",
        help="Get your free API key at https://aistudio.google.com/app/apikey"
    )

    api_key = api_key_input.strip() if api_key_input else ""
    if api_key:
        st.markdown('<span class="badge badge-green">🟢 Gemini Live Mode</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-amber">🟡 Demo / Offline Mode</span>', unsafe_allow_html=True)
        st.caption("No key? You can explore all features using Demo Plans or get a key at [Google AI Studio](https://aistudio.google.com/).")

    st.markdown("---")

    # Model Selection
    model_name = st.selectbox(
        "🧠 Gemini Model",
        options=["gemini-3.8-flash"],
        index=0,
        help="Gemini 3.8 Flash is Google's active, supported high-speed reasoning model."
    )

    st.markdown("---")

    # Quick Presets Selector
    st.markdown("### 🎯 Quick Persona Presets")
    preset_choice = st.selectbox(
        "Select a profile preset:",
        options=list(PRESETS.keys()),
        index=0
    )

    if st.button("🔄 Apply Preset Data", use_container_width=True):
        st.session_state.active_preset = preset_choice
        st.session_state.workout_plan = None
        st.session_state.meal_plan = None
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #64748b; line-height: 1.5;">
        <b>About FitBuddy:</b><br>
        Combines deterministic biometric formulas (Mifflin-St Jeor, BMI, TDEE) with Google Gemini GenAI to design injury-safe, highly structured workout and nutrition regimes.
        </div>
        """,
        unsafe_allow_html=True
    )


# Load default values from active preset
current_preset = PRESETS.get(st.session_state.active_preset, PRESETS["Fat Loss & Conditioning"])

# --- HERO BANNER ---
st.markdown(
    """
    <div class="hero-header">
        <div class="hero-title">
            <span>⚡ FitBuddy</span>
            <span style="font-size: 1rem; vertical-align: middle;" class="badge badge-green">GenAI Powered</span>
        </div>
        <div class="hero-subtitle">
            Hyper-personalized fitness & nutrition architectures powered by Google Gemini Models. 
            Deterministic metabolic science combined with generative intelligence.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- TOP LEVEL TABS ---
tab_profile, tab_workout, tab_nutrition, tab_coach, tab_export = st.tabs([
    "📋 Assessment & Profile",
    "🏋️ Workout Blueprint",
    "🥗 Nutrition & Meal Plan",
    "💬 FitBuddy AI Coach",
    "📑 Plan Exporter & Summary"
])

# -------------------------------------------------------------
# TAB 1: ASSESSMENT & HEALTH PROFILE
# -------------------------------------------------------------
with tab_profile:
    st.markdown("### 👤 Biometrics & Training Preferences")
    st.caption("Adjust your stats below to calculate your real-time metabolic benchmarks.")

    col1, col2, col3 = st.columns([1.2, 1.2, 1.2])

    with col1:
        st.markdown("#### 1. Physical Biometrics")
        age = st.number_input("Age (years)", min_value=14, max_value=90, value=int(current_preset["age"]), step=1)
        gender = st.selectbox("Biological Gender", options=["Male", "Female"], index=0 if current_preset["gender"] == "Male" else 1)
        height_cm = st.number_input("Height (cm)", min_value=120.0, max_value=230.0, value=float(current_preset["height_cm"]), step=0.5)
        weight_kg = st.number_input("Current Weight (kg)", min_value=35.0, max_value=220.0, value=float(current_preset["weight_kg"]), step=0.5)
        target_weight_kg = st.number_input("Target Goal Weight (kg)", min_value=35.0, max_value=220.0, value=float(current_preset["target_weight_kg"]), step=0.5)

    with col2:
        st.markdown("#### 2. Goal & Experience")
        goal_options = [
            "Fat Loss / Caloric Deficit",
            "Muscle Gain / Hypertrophy",
            "Body Recomposition (Lose Fat + Build Muscle)",
            "Cardiovascular Endurance",
            "General Fitness & Mobility"
        ]
        goal_idx = 0
        for i, g in enumerate(goal_options):
            if current_preset["goal"] in g or g in current_preset["goal"]:
                goal_idx = i
                break
        goal = st.selectbox("Primary Fitness Objective", options=goal_options, index=goal_idx)

        activity_options = [
            "Sedentary (desk job, little to no exercise)",
            "Lightly Active (1-3 days exercise/week)",
            "Moderately Active (3-5 days exercise/week)",
            "Very Active (6-7 days hard exercise/week)",
            "Extremely Active (athlete / physical labor job)"
        ]
        act_idx = 2
        for i, a in enumerate(activity_options):
            if current_preset["activity_level"][:15] in a:
                act_idx = i
                break
        activity_level = st.selectbox("Daily Activity Level", options=activity_options, index=act_idx)

        experience = st.selectbox(
            "Training Experience",
            options=["Beginner (< 6 months)", "Intermediate (1 - 3 years)", "Advanced (3+ years)"],
            index=1 if "Inter" in current_preset["experience"] else (0 if "Beg" in current_preset["experience"] else 2)
        )

        equipment = st.selectbox(
            "Available Equipment",
            options=["Full Gym Access", "Dumbbells & Bench", "Bodyweight & Resistance Bands", "Kettlebells Only"],
            index=0 if "Full" in current_preset["equipment"] else (2 if "Body" in current_preset["equipment"] else 1)
        )

    with col3:
        st.markdown("#### 3. Schedule & Nutrition")
        days_val = max(2, min(6, int(current_preset.get("days_per_week", 4))))
        days_per_week = st.slider("Workout Days Per Week", min_value=2, max_value=6, value=days_val)

        duration_options = [20, 30, 45, 50, 60, 75, 90, 120]
        preset_duration = int(current_preset.get("session_duration_mins", 45))
        duration_val = preset_duration if preset_duration in duration_options else min(duration_options, key=lambda x: abs(x - preset_duration))

        session_duration = st.select_slider(
            "Session Duration (minutes)",
            options=duration_options,
            value=duration_val
        )

        diet_options = [
            "High Protein Omnivore",
            "Clean Bulking (High Carb & Protein)",
            "Vegetarian",
            "Vegan (Plant-Based)",
            "Keto / Low-Carb",
            "Mediterranean Balanced"
        ]
        diet_idx = 0
        preset_dt = current_preset.get("diet_type", "").lower()
        for i, d in enumerate(diet_options):
            if current_preset.get("diet_type", "")[:5].lower() in d.lower() or any(w in d.lower() for w in preset_dt.split() if len(w) > 4):
                diet_idx = i
                break
        diet_type = st.selectbox("Dietary Preference", options=diet_options, index=diet_idx)

        allergies = st.text_input("Allergies or Dislikes", value=current_preset.get("allergies", "None"))
        injuries = st.text_input("Physical Limitations / Joint Issues", value=current_preset.get("injuries", "None"))

    # Save gathered profile into a dictionary
    user_profile = {
        "age": age,
        "gender": gender,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "target_weight_kg": target_weight_kg,
        "goal": goal,
        "activity_level": activity_level,
        "experience": experience,
        "equipment": equipment,
        "days_per_week": days_per_week,
        "session_duration_mins": session_duration,
        "diet_type": diet_type,
        "allergies": allergies,
        "injuries": injuries
    }

    # Deterministic Health Calculations
    bmi_data = calculate_bmi(weight_kg, height_cm)
    bmr_val = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee_val = calculate_tdee(bmr_val, activity_level)
    target_cals_data = calculate_target_calories(tdee_val, goal)
    macros_data = calculate_macros(target_cals_data["target_calories"], weight_kg, goal)
    hydration_l = calculate_hydration(weight_kg, session_duration)
    ideal_w_min, ideal_w_max = get_ideal_weight_range(height_cm)

    calculated_metrics = {
        "bmi": bmi_data["bmi"],
        "bmi_category": bmi_data["category"],
        "bmi_color": bmi_data["color"],
        "bmr": bmr_val,
        "tdee": tdee_val,
        "target_calories": target_cals_data["target_calories"],
        "calorie_mode": target_cals_data["mode"],
        "calorie_delta": target_cals_data["delta"],
        "macros": macros_data,
        "hydration_l": hydration_l,
        "ideal_weight_range": f"{ideal_w_min} - {ideal_w_max} kg"
    }

    st.markdown("---")
    st.markdown("### 📊 Real-Time Metabolic & Biometric Benchmarks")

    # Metrics Card Grid
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)

    with mcol1:
        st.markdown(
            f"""
            <div class="stat-card">
                <span class="stat-icon">⚖️</span>
                <div class="stat-label">Body Mass Index</div>
                <div class="stat-value">{calculated_metrics['bmi']}</div>
                <div class="stat-subtext">
                    <span class="badge" style="background-color: {bmi_data['color']}22; color: {bmi_data['color']}; border: 1px solid {bmi_data['color']}55;">
                        {calculated_metrics['bmi_category']}
                    </span>
                </div>
                <div style="font-size: 0.75rem; color: #64748b; margin-top: 6px;">Ideal: {calculated_metrics['ideal_weight_range']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with mcol2:
        st.markdown(
            f"""
            <div class="stat-card">
                <span class="stat-icon">🔥</span>
                <div class="stat-label">Basal Metabolic Rate</div>
                <div class="stat-value">{calculated_metrics['bmr']} <span style="font-size: 1rem; color:#94a3b8;">kcal</span></div>
                <div class="stat-subtext">Base burn at complete rest (Mifflin-St Jeor)</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with mcol3:
        st.markdown(
            f"""
            <div class="stat-card">
                <span class="stat-icon">⚡</span>
                <div class="stat-label">Total Daily Energy (TDEE)</div>
                <div class="stat-value">{calculated_metrics['tdee']} <span style="font-size: 1rem; color:#94a3b8;">kcal</span></div>
                <div class="stat-subtext">Maintenance level with activity</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with mcol4:
        delta_str = f"+{calculated_metrics['calorie_delta']}" if calculated_metrics['calorie_delta'] > 0 else f"{calculated_metrics['calorie_delta']}"
        st.markdown(
            f"""
            <div class="stat-card" style="border-color: rgba(16, 185, 129, 0.4);">
                <span class="stat-icon">🎯</span>
                <div class="stat-label">Target Daily Calories</div>
                <div class="stat-value" style="color: #34d399;">{calculated_metrics['target_calories']} <span style="font-size: 1rem; color:#94a3b8;">kcal</span></div>
                <div class="stat-subtext"><span class="badge badge-green">{calculated_metrics['calorie_mode']}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Macronutrient Breakdown Bar
    st.markdown("#### 🥗 Daily Macronutrient & Hydration Targets")
    m = calculated_metrics["macros"]
    st.markdown(
        f"""
        <div class="macro-bar-container">
            <div class="macro-segment macro-protein" style="width: {m['protein_pct']}%;" title="Protein {m['protein_pct']}%"></div>
            <div class="macro-segment macro-carbs" style="width: {m['carbs_pct']}%;" title="Carbs {m['carbs_pct']}%"></div>
            <div class="macro-segment macro-fat" style="width: {m['fat_pct']}%;" title="Fat {m['fat_pct']}%"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    macro_col1, macro_col2, macro_col3, macro_col4 = st.columns(4)
    with macro_col1:
        st.markdown(f"🥩 **Protein:** **{m['protein_g']}g** ({m['protein_pct']}%) • *Muscle synthesis & recovery*")
    with macro_col2:
        st.markdown(f"🍚 **Carbohydrates:** **{m['carbs_g']}g** ({m['carbs_pct']}%) • *Workout energy fuel*")
    with macro_col3:
        st.markdown(f"🥑 **Healthy Fats:** **{m['fat_g']}g** ({m['fat_pct']}%) • *Hormonal balance*")
    with macro_col4:
        st.markdown(f"💧 **Hydration Target:** **{calculated_metrics['hydration_l']} L/day**")

# -------------------------------------------------------------
# TAB 2: WORKOUT BLUEPRINT
# -------------------------------------------------------------
with tab_workout:
    st.markdown("### 🏋️ Custom Workout Architecture")
    st.caption("AI-engineered training splits tailored to your available equipment and injury precautions.")

    btn_col1, btn_col2, _ = st.columns([1.5, 1.5, 3])
    with btn_col1:
        gen_workout = st.button("⚡ Generate AI Workout Plan", use_container_width=True)
    with btn_col2:
        load_demo_workout = st.button("📋 Load Demo Workout Plan", use_container_width=True)

    if load_demo_workout:
        st.session_state.workout_plan = SAMPLE_WORKOUT_PLAN
        st.success("Loaded demo workout routine!")

    if gen_workout:
        if not api_key:
            st.warning("⚠️ No Gemini API key provided. Loading rich demonstration plan instead. Enter your key in the sidebar for live AI generation.")
            st.session_state.workout_plan = SAMPLE_WORKOUT_PLAN
        else:
            with st.spinner(f"FitBuddy is generating your workout split using {model_name}..."):
                try:
                    sys_prompt, user_prompt = gemini_client.build_workout_prompt(user_profile, calculated_metrics)
                    result = gemini_client.call_gemini(user_prompt, sys_prompt, api_key, model_name)
                    st.session_state.workout_plan = result
                    st.success("Workout plan generated successfully!")
                except Exception as e:
                    err_msg = str(e).lower()
                    if any(k in err_msg for k in ["503", "unavailable", "high demand"]):
                        st.warning("⚠️ Google Gemini servers are experiencing temporary high demand (503). Loaded FitBuddy's calibrated workout routine.")
                    else:
                        st.error(f"Error generating workout plan: {e}")
                        st.info("Falling back to demo workout plan.")
                    st.session_state.workout_plan = SAMPLE_WORKOUT_PLAN

    if st.session_state.workout_plan:
        st.markdown("---")
        st.markdown(st.session_state.workout_plan)
    else:
        st.info("👆 Click **Generate AI Workout Plan** or **Load Demo Workout Plan** above to view your training blueprint.")

# -------------------------------------------------------------
# TAB 3: NUTRITION & MEAL PLAN
# -------------------------------------------------------------
with tab_nutrition:
    st.markdown("### 🥗 Precision Nutrition & Meal Blueprint")
    st.caption(f"Structured to hit your exact **{calculated_metrics['target_calories']} kcal** target ({calculated_metrics['calorie_mode']}).")

    nbtn_col1, nbtn_col2, _ = st.columns([1.5, 1.5, 3])
    with nbtn_col1:
        gen_meal = st.button("⚡ Generate AI Nutrition Plan", use_container_width=True)
    with nbtn_col2:
        load_demo_meal = st.button("📋 Load Demo Meal Plan", use_container_width=True)

    if load_demo_meal:
        st.session_state.meal_plan = SAMPLE_MEAL_PLAN
        st.success("Loaded demo nutrition blueprint!")

    if gen_meal:
        if not api_key:
            st.warning("⚠️ No Gemini API key provided. Loading rich demonstration plan instead. Enter your key in the sidebar for live AI generation.")
            st.session_state.meal_plan = SAMPLE_MEAL_PLAN
        else:
            with st.spinner(f"FitBuddy is formulating your macro blueprint using {model_name}..."):
                try:
                    sys_prompt, user_prompt = gemini_client.build_meal_prompt(user_profile, calculated_metrics)
                    result = gemini_client.call_gemini(user_prompt, sys_prompt, api_key, model_name)
                    st.session_state.meal_plan = result
                    st.success("Nutrition blueprint generated successfully!")
                except Exception as e:
                    err_msg = str(e).lower()
                    if any(k in err_msg for k in ["503", "unavailable", "high demand"]):
                        st.warning("⚠️ Google Gemini servers are experiencing temporary high demand (503). Loaded FitBuddy's calibrated meal blueprint.")
                    else:
                        st.error(f"Error generating meal plan: {e}")
                        st.info("Falling back to demo meal blueprint.")
                    st.session_state.meal_plan = SAMPLE_MEAL_PLAN

    if st.session_state.meal_plan:
        st.markdown("---")
        st.markdown(st.session_state.meal_plan)
    else:
        st.info("👆 Click **Generate AI Nutrition Plan** or **Load Demo Meal Plan** above to view your meal blueprint.")

# -------------------------------------------------------------
# TAB 4: FITBUDDY AI COACH (CHAT)
# -------------------------------------------------------------
with tab_coach:
    st.markdown("### 💬 Ask FitBuddy AI Coach")
    st.caption("Ask questions about technique, recipe swaps, injury rehab, or motivation. Your profile is automatically provided as context.")

    # Suggested Prompts
    st.markdown("**💡 Quick Prompt Starters:**")
    prompt_col1, prompt_col2, prompt_col3 = st.columns(3)
    quick_prompt = None

    if prompt_col1.button("🦵 Knee-friendly squat alternatives"):
        quick_prompt = "What are the best knee-friendly alternatives to heavy barbell back squats that still build strong quads and glutes?"
    if prompt_col2.button("🍳 Quick 30g protein snack under 200 kcal"):
        quick_prompt = "Give me 3 quick, high-protein snack ideas with at least 30g protein and under 250 calories."
    if prompt_col3.button("⚡ Pre-workout meal timing tips"):
        quick_prompt = "What should I eat 60 minutes before a high-intensity workout for optimal energy without stomach discomfort?"

    # Render Conversation History
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user"><b>You:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-assistant"><b>⚡ FitBuddy Coach:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

    # Chat Input Box
    user_query = st.chat_input("Ask FitBuddy a question...")
    effective_query = quick_prompt if quick_prompt else user_query

    if effective_query:
        st.session_state.chat_history.append({"role": "user", "content": effective_query})

        if not api_key:
            demo_answer = (
                f"**Coach FitBuddy:** Great question about *'{effective_query[:45]}...'*\n\n"
                f"Based on your profile ({user_profile['goal']} with {user_profile['equipment']}), here is my advice:\n"
                f"- **Form & Safety:** Always prioritize joint alignment. If you experience discomfort with ({user_profile['injuries']}), utilize unilateral movements like Bulgarian split squats or machine leg presses.\n"
                f"- **Progressive Overload:** Increase resistance by no more than 2.5-5% weekly.\n"
                f"- **Nutritional Fuel:** Keep hitting your daily **{calculated_metrics['target_calories']} kcal** with **{calculated_metrics['macros']['protein_g']}g protein** to support tissue repair.\n\n"
                f"*(Note: Connect your Gemini API Key in the sidebar for live dynamic coaching answers!)*"
            )
            st.session_state.chat_history.append({"role": "assistant", "content": demo_answer})
            st.rerun()
        else:
            with st.spinner("FitBuddy AI Coach is formulating advice..."):
                try:
                    answer = gemini_client.chat_with_coach(
                        st.session_state.chat_history,
                        user_profile,
                        calculated_metrics,
                        api_key,
                        model_name
                    )
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()
                except Exception as e:
                    if hasattr(gemini_client, "generate_coach_offline_response"):
                        fallback_ans = gemini_client.generate_coach_offline_response(effective_query, user_profile, calculated_metrics)
                    else:
                        fallback_ans = (
                            f"**FitBuddy AI Coach (Offline Science Grounding):**\n\n"
                            f"Regarding *\"{effective_query}\"*:\n\n"
                            f"- **Goal Alignment:** For {user_profile['goal']} using {user_profile['equipment']}, stay disciplined with your {user_profile['days_per_week']}-day schedule and {user_profile['session_duration_mins']}-minute training duration.\n"
                            f"- **Metabolic Nutrition:** Hit your daily target of **{calculated_metrics['target_calories']} kcal** with **{calculated_metrics['macros']['protein_g']}g protein** and **{calculated_metrics['hydration_l']}L water**.\n"
                            f"- **Joint Safety:** Honor noted limitation: *{user_profile['injuries']}*.\n\n"
                            f"> *Note: Google Gemini servers are experiencing temporary high demand (503). This response was synthesized by FitBuddy's metabolic science engine.*"
                        )
                    st.session_state.chat_history.append({"role": "assistant", "content": fallback_ans})
                    st.rerun()

# -------------------------------------------------------------
# TAB 5: EXPORT & SUMMARY
# -------------------------------------------------------------
with tab_export:
    st.markdown("### 📑 Complete Consolidated Fitness & Nutrition Dossier")
    st.caption("Review your full regimen or download it as a clean Markdown dossier to save or print.")

    # Build Consolidated Document
    summary_markdown = f"""# ⚡ FitBuddy AI: Personalized Health & Training Dossier
*Generated by Google Cloud Generative AI & Gemini*

---

## 1. Athlete Assessment & Biometrics
- **Age:** {user_profile['age']} | **Gender:** {user_profile['gender']}
- **Height:** {user_profile['height_cm']} cm | **Current Weight:** {user_profile['weight_kg']} kg (Target: {user_profile['target_weight_kg']} kg)
- **Primary Goal:** {user_profile['goal']}
- **Training Experience:** {user_profile['experience']}
- **Available Equipment:** {user_profile['equipment']}
- **Frequency:** {user_profile['days_per_week']} days/week ({user_profile['session_duration_mins']} mins/session)
- **Injuries / Limitations:** {user_profile['injuries']}

## 2. Metabolic Science & Energy Targets
- **Body Mass Index (BMI):** {calculated_metrics['bmi']} ({calculated_metrics['bmi_category']})
- **Ideal Weight Range:** {calculated_metrics['ideal_weight_range']}
- **Basal Metabolic Rate (BMR):** {calculated_metrics['bmr']} kcal/day
- **Total Daily Energy Expenditure (TDEE):** {calculated_metrics['tdee']} kcal/day
- **Daily Target Intake:** {calculated_metrics['target_calories']} kcal/day ({calculated_metrics['calorie_mode']})
- **Macronutrient Split:**
  - 🥩 Protein: {calculated_metrics['macros']['protein_g']}g ({calculated_metrics['macros']['protein_pct']}%)
  - 🍚 Carbohydrates: {calculated_metrics['macros']['carbs_g']}g ({calculated_metrics['macros']['carbs_pct']}%)
  - 🥑 Healthy Fats: {calculated_metrics['macros']['fat_g']}g ({calculated_metrics['macros']['fat_pct']}%)
- **Daily Water Target:** {calculated_metrics['hydration_l']} Liters

---

## 3. Custom Workout Blueprint
{st.session_state.workout_plan if st.session_state.workout_plan else "_Workout plan not generated yet._"}

---

## 4. Custom Nutrition & Meal Blueprint
{st.session_state.meal_plan if st.session_state.meal_plan else "_Meal plan not generated yet._"}

---
*Disclaimer: FitBuddy provides AI-assisted fitness and nutritional guidance based on user inputs. Consult a licensed physician or physical therapist before beginning any strenuous exercise program.*
"""

    st.download_button(
        label="💾 Download Plan as Markdown (.md)",
        data=summary_markdown,
        file_name="FitBuddy_Personalized_Plan.md",
        mime="text/markdown",
        use_container_width=True
    )

    with st.expander("📄 Preview Full Dossier Content", expanded=True):
        st.markdown(summary_markdown)
