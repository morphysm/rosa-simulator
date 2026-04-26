import ollama
from scenario import SCENARIO
from state import state, update_state, reset, get_behavioral_description, history

MODEL = "rosa"

reset()

print("=" * 55)
print("  ROSA SIMULATOR")
print("  Practice communicating with someone in crisis.")
print("  Type 'exit' to end the session and see your debrief.")
print("=" * 55)
print()

conversation_lines = []
turn = 0

while True:
    user_input = input("YOU: ").strip()

    if not user_input:
        continue

    if user_input.lower() == "exit":
        break

    turn += 1

    # Update state based on what the user said, THEN build the prompt
    # so Rosa's behavior immediately reflects the impact of this message.
    update_state(turn, user_input)

    stress_desc, trust_desc, speech_pattern = get_behavioral_description()

    conversation_history = (
        "\n".join(conversation_lines)
        if conversation_lines
        else "(Beginning of conversation.)"
    )

    prompt = f"""You are Rosa. Inhabit her completely.

{SCENARIO}

ROSA'S CURRENT STATE (Stress: {state["stress"]}/10 — Trust: {state["trust"]}/10):

How she feels right now:
{stress_desc}

How she relates to this person right now:
{trust_desc}

How she speaks right now:
{speech_pattern}

CONVERSATION SO FAR:
{conversation_history}

The person says:
"{user_input}"

Respond as Rosa speaking out loud. 1–3 sentences.
Express everything through spoken words only — no asterisks, no stage directions, no actions in parentheses.
If she is frightened, show it in what she says. If she trails off, end the sentence mid-thought with a dash.
Speak the way a real person talks, not a character in a play.

ROSA:"""

    response = ollama.generate(model=MODEL, prompt=prompt)
    reply = response["response"].strip()

    print(f"\nROSA: {reply}\n")

    conversation_lines.append(f"YOU: {user_input}")
    conversation_lines.append(f"ROSA: {reply}")


# --- Session Debrief ---
print()
print("=" * 55)
print("  SESSION DEBRIEF")
print("=" * 55)
print()

if not history:
    print("  No turns completed.")
else:
    col_w = 14
    print(f"  {'Turn':<6}{'Stress':<{col_w}}{'Trust':<{col_w}}What you said that mattered")
    print("  " + "-" * 71)

    for entry in history:
        s = f"{entry['stress_before']}→{entry['stress_after']}"
        t = f"{entry['trust_before']}→{entry['trust_after']}"
        notes = "; ".join(entry["notes"]) if entry["notes"] else "no recognized phrases"
        print(f"  {entry['turn']:<6}{s:<{col_w}}{t:<{col_w}}{notes}")

    print()

    initial_stress = history[0]["stress_before"]
    initial_trust  = history[0]["trust_before"]
    final_stress   = state["stress"]
    final_trust    = state["trust"]

    print(f"  Starting state:  Stress {initial_stress}/10  |  Trust {initial_trust}/10")
    print(f"  Final state:     Stress {final_stress}/10  |  Trust {final_trust}/10")
    print()

    stress_delta = final_stress - initial_stress
    trust_delta  = final_trust  - initial_trust

    if stress_delta < -2:
        print("  → Rosa's distress SIGNIFICANTLY DECREASED — strong de-escalation.")
    elif stress_delta < 0:
        print(f"  → Rosa's distress decreased by {abs(stress_delta)} point(s).")
    elif stress_delta == 0:
        print("  → Rosa's distress was unchanged.")
    else:
        print(f"  → Rosa's distress INCREASED by {stress_delta} point(s) — review what escalated her.")

    if trust_delta > 2:
        print("  → Rosa's trust SIGNIFICANTLY INCREASED — she felt safe with you.")
    elif trust_delta > 0:
        print(f"  → Rosa's trust increased by {trust_delta} point(s) — she began to open up.")
    elif trust_delta == 0:
        print("  → Rosa's trust was unchanged.")
    else:
        print(f"  → Rosa's trust DECREASED by {abs(trust_delta)} point(s) — she felt less safe with you.")

    print()

    best  = max(history, key=lambda e: (e["stress_before"] - e["stress_after"]) + (e["trust_after"]  - e["trust_before"]))
    worst = max(history, key=lambda e: (e["stress_after"]  - e["stress_before"]) + (e["trust_before"] - e["trust_after"]))

    best_score  = (best["stress_before"]  - best["stress_after"])  + (best["trust_after"]  - best["trust_before"])
    worst_score = (worst["stress_after"]  - worst["stress_before"]) + (worst["trust_before"] - worst["trust_after"])

    if best_score > 0:
        print(f"  Best moment    (Turn {best['turn']}): \"{best['user_input']}\"")
    if worst_score > 0:
        print(f"  Hardest moment (Turn {worst['turn']}): \"{worst['user_input']}\"")

print()
print("  Thank you for practicing with Rosa.")
print()
