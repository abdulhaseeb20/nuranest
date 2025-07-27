TIMELINE_RULES = [
    {
        "min_week": 4,
        "max_week": 8,
        "symptoms": ["severe abdominal pain", "shoulder pain", "dizziness", "heavy bleeding"],
        "condition": "Ectopic Pregnancy",
        "risk": "High",
        "action": "Emergency OB-GYN evaluation"
    },
    {
        "min_week": 20,
        "max_week": 40,
        "symptoms": ["blurry vision", "headache", "swelling", "high blood pressure"],
        "condition": "Preeclampsia",
        "risk": "High",
        "action": "Urgent prenatal evaluation"
    },
    {
        "min_week": 28,
        "max_week": 40,
        "symptoms": ["no fetal movement", "reduced fetal movement"],
        "condition": "Stillbirth or Fetal Distress",
        "risk": "High",
        "action": "Immediate fetal heart check"
    },
    {
        "min_week": 1,
        "max_week": 12,
        "symptoms": ["spotting", "fatigue", "severe cramping"],
        "condition": "Possible Miscarriage",
        "risk": "Medium–High",
        "action": "Ultrasound recommended"
    },
    {
        "min_week": 13,
        "max_week": 27,
        "symptoms": ["contractions", "pelvic pressure", "watery discharge"],
        "condition": "Preterm Labor",
        "risk": "Medium–High",
        "action": "Hospital evaluation if < 37 weeks"
    }
]
