# 🔬 FitBuddy: Metabolic Science Engine

This document details the scientific equations, physiological models, and deterministic logic implemented in [`calculator.py`](file:///c:/Users/ADMIN/.gemini/antigravity-ide/scratch/fitbuddy/calculator.py).

---

## 1. Body Mass Index (BMI) & Ideal Weight Range

### Formulation
$$\text{BMI} = \frac{\text{Weight (kg)}}{(\text{Height (m)})^2}$$

### WHO Classification & Action Thresholds
| BMI Range | WHO Classification | Color Code | Clinical Recommendation |
| :--- | :--- | :--- | :--- |
| `< 18.5` | Underweight | `#38bdf8` (Cyan) | Mild caloric surplus (+200-300 kcal), focus on lean muscle mass acquisition. |
| `18.5 – 24.9` | Normal / Healthy | `#10b981` (Emerald) | Optimal baseline. Focus on body recomposition and cardiovascular fitness. |
| `25.0 – 29.9` | Overweight (Pre-obese) | `#f59e0b` (Amber) | Modest caloric deficit (-400-500 kcal) with high protein to protect lean tissue. |
| `≥ 30.0` | Obese | `#ef4444` (Rose) | Sustainable, gradual fat loss with low-impact joint movements. |

### Ideal Weight Calculation
Derived using the bounds of the WHO normal BMI window ($18.5 \le \text{BMI} \le 24.9$):
$$\text{Weight}_{\text{min}} = 18.5 \times (\text{Height in meters})^2$$
$$\text{Weight}_{\text{max}} = 24.9 \times (\text{Height in meters})^2$$

---

## 2. Basal Metabolic Rate (BMR)

FitBuddy uses the **Mifflin-St Jeor Equation**, recognized as the most accurate clinical formula for resting metabolic expenditure in non-clinical settings:

### Men:
$$\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age (years)} + 5$$

### Women:
$$\text{BMR} = 10 \times \text{weight (kg)} + 6.25 \times \text{height (cm)} - 5 \times \text{age (years)} - 161$$

*Note: Output is constrained to a physiological minimum of 800 kcal.*

---

## 3. Total Daily Energy Expenditure (TDEE)

TDEE accounts for non-exercise activity thermogenesis (NEAT), exercise activity thermogenesis (EAT), and the thermic effect of food (TEF):

$$\text{TDEE} = \text{BMR} \times \text{Activity Multiplier}$$

| Activity Level Description | Multiplier |
| :--- | :--- |
| Sedentary (desk job, little to no exercise) | `1.200` |
| Lightly Active (1–3 days exercise/week) | `1.375` |
| Moderately Active (3–5 days exercise/week) | `1.550` |
| Very Active (6–7 days hard exercise/week) | `1.725` |
| Extremely Active (athlete / physical labor job) | `1.900` |

---

## 4. Target Calories & Macronutrient Distribution

### Caloric Targets
* **Fat Loss**: $\text{Target} = \max(\text{TDEE} - 450, 1200)\text{ kcal}$
* **Muscle Hypertrophy**: $\text{Target} = \text{TDEE} + 350\text{ kcal}$
* **Endurance Performance**: $\text{Target} = \text{TDEE} + 150\text{ kcal}$
* **Maintenance / Recomp**: $\text{Target} = \text{TDEE}$

### Macronutrient Gram Calculations
* **Protein** ($4\text{ kcal/g}$):
  * Fat Loss: $2.0\text{ g/kg}$ bodyweight (capped at 40% of total calories) to spare muscle protein during negative nitrogen balance.
  * Muscle Gain: $1.8\text{ g/kg}$ bodyweight.
  * Maintenance / Endurance: $1.6\text{ g/kg}$ bodyweight.
* **Fats** ($9\text{ kcal/g}$):
  * Allocated at 25% (fat loss/hypertrophy) to 28% (maintenance) to maintain endocrine function and hormone synthesis.
* **Carbohydrates** ($4\text{ kcal/g}$):
  * Fills remaining caloric volume for central nervous system and muscular glycogen needs:
    $$\text{Carb Grams} = \frac{\text{Target Calories} - (\text{Protein Grams} \times 4 + \text{Fat Grams} \times 9)}{4}$$

---

## 5. Daily Hydration Modeling

Hydration requirements balance resting cellular needs with exercise thermoregulatory sweat losses:

$$\text{Baseline Water (ml)} = \text{Weight (kg)} \times 35\text{ ml}$$
$$\text{Exercise Water (ml)} = \left(\frac{\text{Daily Workout Minutes}}{30}\right) \times 350\text{ ml}$$
$$\text{Total Daily Target (Liters)} = \frac{\text{Baseline (ml)} + \text{Exercise (ml)}}{1000}$$
