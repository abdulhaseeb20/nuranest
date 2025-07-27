from app.symptom_timeline_rules import TIMELINE_RULES

def check_symptoms_by_week(week: int, user_input: str) -> list:
    user_input = user_input.lower()
    matched_conditions = []

    for rule in TIMELINE_RULES:
        if rule["min_week"] <= week <= rule["max_week"]:
            for symptom in rule["symptoms"]:
                if symptom in user_input:
                    matched_conditions.append({
                        "symptom": symptom,
                        "condition": rule["condition"],
                        "risk": rule["risk"],
                        "action": rule["action"],
                        "week": week
                    })

    return matched_conditions
