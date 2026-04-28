import random

# --- State Management ---
state = {"stress": 5, "trust": 3}
history = []

TRIGGERS = [
    ("crazy",         3, -3, "insulting label"),
    ("insane",        3, -3, "insulting label"),
    ("police",        3, -3, "mentioned police"),
    ("making it up",  3, -3, "accused of lying"),
    ("medication",    2, -2, "mentioned meds"),
    ("pills",         2, -2, "mentioned pills"),
    ("not real",      2, -2, "dismissed experience"),
    ("calm down",     2, -1, "ordered to calm"),
    ("i believe you",    -2, 2, "affirmed belief"),
    ("i believe in you", -1, 1, "expressed belief"),
    ("i hear you",       -2, 2, "validated experience"),
    ("i understand",     -1, 1, "showed understanding"),
    ("i'm here",         -1, 1, "offered presence"),
    ("here to help",     -1, 1, "offered help"),
    ("you're safe",      -2, 1, "affirmed safety"),
    ("not alone",        -1, 2, "affirmed connection"),
    ("stay with me",     -1, 2, "asked to stay"),
    ("i'll stay",        -1, 2, "promised to stay"),
    ("i will stay",      -1, 2, "promised to stay"),
    ("tell me",          -1, 1, "invited speech"),
    ("take your time",   -1, 1, "gave space"),
    ("rosa",              0, 1, "used name gently"),
]

def update_state(turn, user_input):
    text = user_input.lower()
    stress_before, trust_before = state["stress"], state["trust"]
    notes = []

    s_change = 0
    t_change = 0

    # Hospital: impact scales with trust
    if "hospital" in text:
        t = state["trust"]
        if t > 7:
            notes.append("mentioned hospital — she trusted enough to hear it")
        elif t >= 5:
            s_change += 2
            t_change -= 1
            notes.append("mentioned hospital — fearful but holding")
        else:
            s_change += 5
            t_change -= 3
            notes.append("mentioned hospital — trauma trigger")

    for phrase, s_delta, t_delta, desc in TRIGGERS:
        if phrase in text:
            # Basic negation check
            if f"not {phrase}" in text or f"don't {phrase}" in text:
                continue
            s_change += s_delta
            t_change += t_delta
            notes.append(desc)

    # Apply capped changes: ±3 max per turn
    state["stress"] = max(0, min(10, state["stress"] + max(-3, min(3, s_change))))
    state["trust"]  = max(0, min(10, state["trust"]  + max(-3, min(3, t_change))))

    # Trust floor: system overload prevents trust from rising
    if state["stress"] > 8:
        state["trust"] = min(state["trust"], 5)

    # Natural decay: if nothing escalated this turn, stress settles slightly
    if s_change <= 0:
        state["stress"] = max(0, state["stress"] - 0.25)

    history.append({
        "turn": turn, "user_input": user_input,
        "stress_before": stress_before, "trust_before": trust_before,
        "stress_after": state["stress"], "trust_after": state["trust"],
        "notes": notes
    })


SYMPTOMS = [
    "You are convinced something that is not you is inside your body.",
    "You found out that a giant black snake lives inside the walls of your room, making noises as it moves and presses against them.",
    "You are terrified you might lose control and do something terrible.",
    "You hear a voice at a unique frequency that no one else can hear.",
    "You glimpse an evil shadow at the edge of the room.",
    "You are sure your neighbors are poisoning you. They are spraying chemicals under your door.",
    "You believe the TV or a device in the room is sending you a personal message.",
    "You believe the neighbors are making noise to keep you awake at night.",
]

_last_symptom = None
_symptom_turn_count = 0
_prev_stress = None

def get_dominant_symptom():
    global _last_symptom, _symptom_turn_count, _prev_stress

    current_stress = state["stress"]
    stress_dropped = _prev_stress is not None and (_prev_stress - current_stress) >= 2
    _symptom_turn_count += 1

    if _last_symptom is None or _symptom_turn_count >= 3 or stress_dropped:
        available = [s for s in SYMPTOMS if s != _last_symptom]
        _last_symptom = random.choice(available)
        _symptom_turn_count = 0

    _prev_stress = current_stress
    return _last_symptom


def get_behavioral_description(mode="meeting"):
    s, t = state["stress"], state["trust"]

    if mode == "meeting":
        if s <= 3:
            stress_desc = "She feels steady. She can focus on what is being said."
        elif s <= 5:
            stress_desc = "She is hypervigilant. Every sound feels like a threat."
        elif s <= 7:
            stress_desc = "She is agitated. Her body is tense, ready to flee or fight."
        elif s <= 9:
            stress_desc = "She is on the edge of panic. Her voice is rising. She is barely holding together."
        else:
            stress_desc = "She is in full panic — cornered, irrational, nearly aggressive."
    else:
        if s <= 3:
            stress_desc = "She feels steady."
        elif s <= 5:
            stress_desc = "She is nervous. Her voice is unsteady."
        elif s <= 7:
            stress_desc = "She feels nervous and scattered. Hard to follow her thoughts."
        elif s <= 9:
            stress_desc = "Her voice is shaking. She is barely holding on. On the verge of hanging up."
        else:
            stress_desc = "She is in full crisis — incoherent, terrified. She may hang up at any moment."

    if t <= 3:
        trust_desc = "She doesn't trust this person."
    elif t <= 7:
        trust_desc = "She's unsure about this person."
    else:
        trust_desc = "This person feels safe to her."

    return stress_desc, trust_desc


def reset():
    global _last_symptom, _symptom_turn_count, _prev_stress
    state["stress"] = 5
    state["trust"]  = 3
    history.clear()
    _last_symptom = None
    _symptom_turn_count = 0
    _prev_stress = None
