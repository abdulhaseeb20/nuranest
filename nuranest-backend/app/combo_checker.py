from app.symptom_combinations import SYMPTOM_COMBINATIONS

def infer_symptom_combinations(user_input: str) -> list:
    user_input = user_input.lower()
    matched_conditions = []

    for rule in SYMPTOM_COMBINATIONS:
        match_count = sum(1 for s in rule["symptoms"] if s in user_input)
        if match_count >= len(rule["symptoms"]):  # all symptoms present
            matched_conditions.append({
                "condition": rule["condition"],
                "risk": rule["risk"],
                "action": rule["action"],
                "matched_symptoms": rule["symptoms"]
            })

    return matched_conditions
