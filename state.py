import ollama
from scenario import SCENARIO

# --- State Management ---
state = {"stress": 5, "trust": 3}
history = []

TRIGGERS = [
    ("not real", 2, -2, "dismissed Rosa's experience"), ("imagining", 2, -2, "implied imagination"),
    ("making it up", 3, -3, "accused of lying"), ("that's not true", 1, -1, "contradicted directly"),
    ("nothing is there", 2, -2, "denied perception"), ("there is nobody", 2, -2, "denied presence"),
    ("it's in your head", 2, -2, "internalized the cause"), ("calm down", 2, -1, "ordered to calm"),
    ("just relax", 1, -1, "told to relax"), ("overreacting", 2, -2, "dismissed reaction"),
    ("paranoid", 2, -2, "clinical label"), ("crazy", 3, -3, "insulting label"),
    ("insane", 3, -3, "insulting label"), ("hospital", 2, -2, "mentioned hospital"),
    ("medication", 2, -2, "mentioned meds"), ("pills", 2, -2, "mentioned pills"),
    ("doctor", 1, -1, "mentioned doctor"), ("police", 3, -3, "mentioned police"),
    ("i'm here", -1, 1, "offered presence"), ("you're safe", -2, 1, "affirmed safety"),
    ("i hear you", -2, 2, "validated experience"), ("tell me", -1, 1, "invited speech"),
    ("must be scary", -2, 2, "empathized with fear"), ("i believe you", -2, 2, "affirmed belief"),
    ("take your time", -1, 1, "gave space"), ("i'll stay", -1, 2, "promised to stay"),
    ("not alone", -1, 2, "affirmed connection"), ("rosa", 0, 1, "used name gently")
]

def update_state(turn, user_input):
    text = user_input.lower()
    stress_before, trust_before = state["stress"], state["trust"]
    notes = []
    for phrase, s_delta, t_delta, desc in TRIGGERS:
        if phrase in text:
            state["stress"] = max(0, min(10, state["stress"] + s_delta))
            state["trust"] = max(0, min(10, state["trust"] + t_delta))
            notes.append(desc)
    history.append({
        "turn": turn, "user_input": user_input,
        "stress_before": stress_before, "trust_before": trust_before,
        "stress_after": state["stress"], "trust_after": state["trust"],
        "notes": notes
    })

def get_sensory_state():
    s, t = state["stress"], state["trust"]
    if s <= 3:
        stress_desc, speech = "You feel steady. You can focus.", "Speak in 3 to 5 full sentences."
    elif s <= 7:
        stress_desc, speech = "Your skin is prickly. You hear noises.", "Speak in 3 to 5 jagged, nervous sentences."
    else:
        stress_desc, speech = "Your heart is racing. The voices are loud.", "Speak in 3 to 5 urgent, repetitive fragments."

    if t <= 3:
        trust_desc = "This person feels like a threat. Keep back."
    elif t <= 7:
        trust_desc = "You want to trust them, but you are waiting for a lie."
    else:
        trust_desc = "This person is your anchor. Stay close."
    return stress_desc, trust_desc, speech

# --- Loop ---
MODEL = "rosa"
print("=" * 55 + "\n   ROSA SIMULATOR (AUTHENTIC MODE)\n" + "=" * 55 + "\n")

conversation_lines = []
turn = 0

while True:
    user_input = input("YOU: ").strip()
    if not user_input: continue
    if user_input.lower() == "exit": break

    turn += 1
    update_state(turn, user_input)
    stress_msg, trust_msg, speech_msg = get_sensory_state()

    # Fixed prompt for length and no-theatricals
    prompt = f"""
{SCENARIO}

ROSA'S STATE:
- {stress_msg}
- {trust_msg}
- {speech_msg}

RECENT HISTORY:
{" ".join(conversation_lines[-6:])}

INPUT:
The person says: "{user_input}"

TASK:
Respond as Rosa. 
- Use ONLY spoken dialogue. 
- Length: 3 to 5 sentences.
- NO asterisks (*), NO stage directions, NO sound effects (like *knock*).
- If you hear something, say: "I hear a sound," do not type the sound itself.

ROSA:"""

    response = ollama.generate(
        model=MODEL, 
        prompt=prompt,
        options={
            "temperature": 0.8,
            "num_predict": 200,
            "stop": ["YOU:", "ROSA:", "\n", "*", "(", "[", " *", "—*"]
        }
    )
    
    reply = response["response"].strip().replace('"', '')
    print(f"\nROSA: {reply}\n")
    
    conversation_lines.append(f"YOU: {user_input}")
    conversation_lines.append(f"ROSA: {reply}")

# --- Debrief ---
print("\n" + "=" * 55 + "\n   SESSION DEBRIEF\n" + "=" * 55)
for e in history:
    print(f"Turn {e['turn']}: {e['stress_before']}->{e['stress_after']} Stress | {', '.join(e['notes']) if e['notes'] else 'neutral'}")