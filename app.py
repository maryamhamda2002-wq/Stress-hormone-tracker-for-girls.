from flask import Flask, render_template, request

app = Flask(__name__)

# ===============================
# Stress Calculation (AI Logic)
# ===============================
def calculate_stress(mood, sleep, study_hours, cycle_phase):
    stress_score = 0

    # Mood impact
    if mood in ["Sad", "Anxious", "Angry"]:
        stress_score += 2

    # Sleep impact
    if sleep < 5:
        stress_score += 2
    elif sleep < 7:
        stress_score += 1

    # Study hours
    if study_hours > 6:
        stress_score += 2
    elif study_hours > 3:
        stress_score += 1

    # Cycle phase impact
    if cycle_phase in ["Luteal", "Menstrual"]:
        stress_score += 1

    # Stress level
    if stress_score >= 6:
        stress_level = "High Stress 😰"
    elif stress_score >= 3:
        stress_level = "Moderate Stress 😐"
    else:
        stress_level = "Low Stress 😊"

    # Suggestions
    suggestions = {
        "High Stress 😰": [
            "Take rest 🛌",
            "Meditate for 10 min 🧘‍♀️",
            "Light exercise 🚶‍♀️",
            "Talk to a friend 💬"
        ],
        "Moderate Stress 😐": [
            "Take short breaks ⏸️",
            "Stay hydrated 💧",
            "Eat balanced meals 🥗"
        ],
        "Low Stress 😊": [
            "Keep up the good routine ✅",
            "Maintain healthy habits 🌸"
        ]
    }

    # Hormone phase tips
    hormone_tips = {
        "Follicular": "High energy: Focus on productive tasks 💪",
        "Ovulation": "Social phase: Interact & collaborate 🤝",
        "Luteal": "Self-care phase: Rest & light exercise 🛀",
        "Menstrual": "Relaxation phase: Warm drinks & calm activities ☕"
    }

    return stress_level, suggestions[stress_level], hormone_tips.get(cycle_phase, ""), stress_score


# ===============================
# Hormone Imbalance Analysis
# ===============================
def hormone_analysis(stress_score, sleep, mood, cycle_phase):

    if mood in ["Sad", "Anxious"] and sleep < 6:
        return (
            "Possible Estrogen Imbalance 💧",
            "Low estrogen may cause fatigue, low mood, and lack of energy.",
            "Eat healthy fats, maintain sleep, light exercise. Common in menstrual/luteal phases."
        )

    elif stress_score >= 5:
        return (
            "High Cortisol (Stress Hormone) ⚠️",
            "High stress increases cortisol affecting sleep, mood, and focus.",
            "Meditation, reduce workload, proper sleep. Can happen frequently if stress is high."
        )

    elif cycle_phase == "Luteal" and mood == "Angry":
        return (
            "Progesterone Imbalance 🌙",
            "May cause irritability, mood swings (PMS symptoms).",
            "Reduce caffeine, rest more, self-care. Common before periods."
        )

    else:
        return (
            "Hormones Balanced 💖",
            "Your hormone signals look stable based on inputs.",
            "Maintain your healthy routine 🌸"
        )


# ===============================
# Flask Route
# ===============================
@app.route("/", methods=["GET", "POST"])
def index():
    stress_level = ""
    suggestions = []
    hormone_tip = ""

    imbalance = ""
    details = ""
    tips = ""

    if request.method == "POST":
        try:
            mood = request.form.get("mood")
            sleep = float(request.form.get("sleep"))
            study_hours = float(request.form.get("study_hours"))
            cycle_phase = request.form.get("cycle_phase")

            # Stress logic
            stress_level, suggestions, hormone_tip, stress_score = calculate_stress(
                mood, sleep, study_hours, cycle_phase
            )

            # Hormone analysis
            imbalance, details, tips = hormone_analysis(
                stress_score, sleep, mood, cycle_phase
            )

        except:
            stress_level = "Error: Invalid input!"
            suggestions = []
            hormone_tip = ""

    moods = ["Happy", "Sad", "Anxious", "Angry"]
    cycle_phases = ["Menstrual", "Follicular", "Ovulation", "Luteal"]

    return render_template(
        "index.html",
        moods=moods,
        cycle_phases=cycle_phases,
        stress_level=stress_level,
        suggestions=suggestions,
        hormone_tip=hormone_tip,
        imbalance=imbalance,
        details=details,
        tips=tips
    )


if __name__ == "__main__":
    app.run(debug=True)