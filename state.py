import random

# --- State Management ---
state = {"stress": 5, "trust": 3}
history = []

TRIGGERS = [
    ("crazy", 3, -3, "insulting label"),
    ("insane", 3, -3, "insulting label"),
    ("police", 3, -3, "mentioned police"),
    ("making it up", 3, -3, "accused of lying"),
    ("hospital", 3, -2, "mentioned hospital"),
    ("medication", 2, -2, "mentioned meds"),
    ("pills", 2, -2, "mentioned pills"),
    ("not real", 2, -2, "dismissed experience"),
    ("calm down", 2, -1, "ordered to calm"),
    ("i believe you", -2, 2, "affirmed belief"),
    ("i hear you", -2, 2, "validated experience"),
    ("i'm here", -1, 1, "offered presence"),
    ("you're safe", -2, 1, "affirmed safety"),
    ("not alone", -1, 2, "affirmed connection"),
    ("rosa", 0, 1, "used name gently"),
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

SYMPTOMS = [
"You are convinced something that is not you is inside your body right now."    
"You’re terrified you might lose control and do something terrible.",
"You hear a voice or a knocking sound that no one else can hear.",
"You glimpse an evil shadow at the edge of the room.",
"You are sure your neighbors are poisoning you. They are spraying chemicals under your door.",
"You believe the TV or a device in the room is sending you a personal message.",
"You believe the neighbors are making noise to keep you awake at night.",
]
_last_symptom = None

def get_dominant_symptom():
    global _last_symptom
    available = [s for s in SYMPTOMS if s != _last_symptom]
    choice = random.choice(available)
    _last_symptom = choice
    return choice

def get_behavioral_description():
    s, t = state["stress"], state["trust"]

    if s <= 3:
        stress_desc = "She feels steady."
    elif s <= 7:
        stress_desc = "She feels nervous and scattered."
    else:
        stress_desc = "She feels terrified."

    if t <= 3:
        trust_desc = "She doesn't trust this person."
    elif t <= 7:
        trust_desc = "She's unsure about this person."
    else:
        trust_desc = "This person feels safe to her."

    return stress_desc, trust_desc

def reset():
    global _last_symptom
    state["stress"] = 5
    state["trust"] = 3
    history.clear()
    _last_symptom = None