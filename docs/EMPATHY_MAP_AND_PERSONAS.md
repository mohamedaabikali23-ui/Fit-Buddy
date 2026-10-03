# 🎯 FitBuddy: Empathy Map & Athlete Personas

This document details the user personas and design research artifacts developed for **FitBuddy**, specifically matching the **SmartBridge / SkillWallet** evaluation standards (Team ID: `SB-FIT-2024-08`).

---

## 1. Primary Persona: Alex Carter

| Field | Detail |
| :--- | :--- |
| **Name & Age** | Alex Carter (28 years old) |
| **Role / Background** | Working Professional / Fitness Novice |
| **Domain** | AI Healthcare & Sports Nutrition |
| **Primary Goal** | Fat loss without joint pain or unsustainable diet burnout |
| **Key Safeguard** | Knee stiffness on deep knee flexion, lower-back desk fatigue |

---

## 2. The 4-Quadrant Empathy Map

```text
┌───────────────────────────────────────┬───────────────────────────────────────┐
│                 SAYS                  │                 THINKS                │
│                                       │                                       │
│ • "I don't have 2 hours a day to     │ • "Am I executing these exercises     │
│   spend at the gym or cook complex   │   with safe posture, or setting       │
│   recipes."                          │   myself up for injury?"              │
│ • "Personal trainers and dietitians   │ • "Generic 2,000-calorie diets        │
│   are way too expensive for my        │   online never match my metabolism."  │
│   monthly budget."                    │ • "I wish I had a private 24/7 AI     │
│ • "There is so much conflicting advice│   coach I could ask questions to      │
│   on social media."                   │   without feeling judged."            │
│ • "I want a routine that takes into   │ • "Will I stay disciplined this time, │
│   account my knee stiffness."         │   or quit after two weeks?"           │
├───────────────────────────────────────┼───────────────────────────────────────┤
│                 DOES                  │                 FEELS                 │
│                                       │                                       │
│ • Sits at an office desk 8+ hours a  │ • Overwhelmed by excessive,           │
│   day, leading to tight hip flexors.  │   contradictory fitness advice.       │
│ • Starts random online workouts but   │ • Self-conscious entering crowded gym  │
│   quits due to knee discomfort.       │   weight rooms without a plan.        │
│ • Tracks calories inconsistently on   │ • Frustrated when working hard        │
│   phone apps without knowing macros.  │   without visible changes on the scale│
│ • Prepares basic meals at home but    │ • Hopeful that a science-backed,      │
│   often defaults to quick takeout.    │   adaptive AI guide will make fitness │
│                                       │   sustainable and injury-free.        │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

---

## 3. Presets & Personas Matrix ([`sample_data.py`](file:///c:/Users/ADMIN/.gemini/antigravity-ide/scratch/fitbuddy/sample_data.py))

FitBuddy comes pre-configured with four athlete archetypes:

### 1. Fat Loss & Conditioning (Alex Carter Preset)
* **Demographics**: 28yo Male, 178 cm, 85 kg (Target: 75 kg).
* **Schedule**: 4 days/week, 45 mins/session.
* **Equipment**: Full Gym Access.
* **Diet**: High Protein Omnivore.
* **Limitation**: Minor knee stiffness on deep squats.

### 2. Muscle Hypertrophy
* **Demographics**: 24yo Male, 182 cm, 72 kg (Target: 80 kg).
* **Schedule**: 5 days/week, 60 mins/session.
* **Equipment**: Full Gym Access.
* **Diet**: Clean Bulking (High Carb & Protein).
* **Limitation**: None.

### 3. Home Workout & Core Tone
* **Demographics**: 31yo Female, 165 cm, 64 kg (Target: 58 kg).
* **Schedule**: 3 days/week, 30 mins/session.
* **Equipment**: Bodyweight & Resistance Bands.
* **Diet**: Vegetarian (Gluten Sensitive).
* **Limitation**: Lower back fatigue from prolonged sitting.

### 4. Endurance & Running
* **Demographics**: 35yo Female, 170 cm, 60 kg (Target: 60 kg).
* **Schedule**: 5 days/week, 50 mins/session.
* **Equipment**: Dumbbells & Outdoor / Treadmill.
* **Diet**: Balanced Whole Foods (Lactose Intolerant).
* **Limitation**: None.

---

## 4. Associated Deliverables
* **Interactive Web Canvas**: Viewable live at `/empathy-map` ([`templates/empathy_map.html`](file:///c:/Users/ADMIN/.gemini/antigravity-ide/scratch/fitbuddy/templates/empathy_map.html)).
* **Word Document Generator**: [`generate_docx.py`](file:///c:/Users/ADMIN/.gemini/antigravity-ide/scratch/fitbuddy/generate_docx.py) formats and outputs `Empathy_Map_FitBuddy.docx`.
