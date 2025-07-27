from app.triage_questions import TRIAGE_QUESTIONS

def run_triage_questions(existing_input: str) -> dict:
    user_data = {"original_input": existing_input}
    remaining = []

    for q in TRIAGE_QUESTIONS:
        if q["key"] not in existing_input.lower():
            remaining.append(q)

    print("\n🤖 Before I assess, I have a few quick questions for clarity:\n")
    for q in remaining[:4]:  # Ask up to 4 follow-ups
        ans = input(f"{q['question']}\nYou: ").strip()
        user_data[q["key"]] = ans

    return user_data
