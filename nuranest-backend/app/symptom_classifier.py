SYMPTOM_KEYWORDS = {
    "mild nausea": {
        "risk": "Low",
        "condition": "Normal 1st trimester symptom",
        "action": "Self-monitor, routine prenatal follow-up"
    },
    "light spotting": {
        "risk": "Low",
        "condition": "Implantation bleeding",
        "action": "Self-monitor"
    },
    "mild back pain": {
        "risk": "Low",
        "condition": "Ligament stretching",
        "action": "Self-monitor"
    },
    "persistent vomiting": {
        "risk": "Medium",
        "condition": "Possible hyperemesis gravidarum",
        "action": "Contact OB if persists"
    },
    "elevated blood pressure": {
        "risk": "Medium",
        "condition": "Monitor for preeclampsia",
        "action": "Consult doctor within 24h"
    },
    "thirst": {
        "risk": "Medium",
        "condition": "Possible gestational diabetes",
        "action": "Ask for glucose test"
    },
    "heavy bleeding": {
        "risk": "High",
        "condition": "Miscarriage or placental abruption",
        "action": "Immediate OB or ER visit"
    },
    "severe abdominal pain": {
        "risk": "High",
        "condition": "Ectopic pregnancy (if early)",
        "action": "Emergency care"
    },
    "blurry vision": {
        "risk": "High",
        "condition": "Preeclampsia",
        "action": "Immediate evaluation"
    },
    "no fetal movement": {
        "risk": "High",
        "condition": "Fetal distress or demise",
        "action": "Emergency scan"
    },
    "fever": {
        "risk": "High",
        "condition": "Possible intrauterine infection",
        "action": "Visit ER"
    },
    "shoulder tip pain": {
        "risk": "High",
        "condition": "Ectopic pregnancy with bleeding",
        "action": "ER"
    },
    # Add more mappings as needed
}

def classify_symptom(user_input: str) -> list:
    user_input = user_input.lower()
    findings = []

    for symptom_phrase, data in SYMPTOM_KEYWORDS.items():
        if symptom_phrase in user_input:
            findings.append({
                "matched_phrase": symptom_phrase,
                **data
            })

    return findings

