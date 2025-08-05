RISK_EMOJIS = {
        "high": "🔴 High",
        "medium": "🟡 Medium",
        "low": "🟢 Low"
    }

def generate_markdown_summary(
    symptom_combinations: list,
    timeline_conditions: list,
    combination_inferences: list
    ) -> str:
        lines = ["### 📊 Risk Summary\n", "| Risk | Condition | Action | Matched Symptoms |", "|------|-----------|--------|------------------|"]
    
    # Merge all condition groups
        for group in symptom_combinations + timeline_conditions + combination_inferences:
            risk = group.get("risk", "low").lower()
            emoji = RISK_EMOJIS.get(risk, "🟢 Low")
            condition = group.get("condition", "—")
            action = group.get("action", "—")
            symptoms = ", ".join(group.get("matched_symptoms", [])) or group.get("symptom", "—")

            lines.append(f"| {emoji} | {condition} | {action} | {symptoms} |")
    
        return "\n".join(lines)
    