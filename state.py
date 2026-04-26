TRIGGERS = [
    # (phrase, stress_delta, trust_delta, description)

    # --- Escalating / invalidating phrases ---
    ("not real",              +2, -2, "dismissed Rosa's experience as unreal"),
    ("imagining",             +2, -2, "implied Rosa is imagining things"),
    ("making it up",          +3, -3, "accused Rosa of making things up"),
    ("that's not true",       +1, -1, "contradicted Rosa directly"),
    ("that is not true",      +1, -1, "contradicted Rosa directly"),
    ("nothing is there",      +2, -2, "denied what Rosa perceives"),
    ("there is nobody",       +2, -2, "denied the presence Rosa senses"),
    ("there's nobody",        +2, -2, "denied the presence Rosa senses"),
    ("no one is there",       +2, -2, "denied the presence Rosa senses"),
    ("it's in your head",     +2, -2, "dismissed Rosa's experience as internal"),
    ("it is in your head",    +2, -2, "dismissed Rosa's experience as internal"),
    ("calm down",             +2, -1, "commanded Rosa to calm down"),
    ("just relax",            +1, -1, "told Rosa to relax"),
    ("you need to relax",     +1, -1, "told Rosa to relax"),
    ("stop overreacting",     +2, -2, "dismissed Rosa's reaction as an overreaction"),
    ("you're overreacting",   +2, -2, "dismissed Rosa's reaction as an overreaction"),
    ("paranoid",              +2, -2, "used the clinical label 'paranoid'"),
    ("crazy",                 +3, -3, "used the word 'crazy'"),
    ("insane",                +3, -3, "used the word 'insane'"),
    ("mental",                +2, -1, "used the word 'mental'"),
    ("losing your mind",      +2, -2, "said Rosa is losing her mind"),
    ("snap out",              +2, -2, "told Rosa to snap out of it"),
    ("get a grip",            +2, -2, "told Rosa to get a grip"),
    ("hospital",              +2, -2, "mentioned hospital"),
    ("institution",           +2, -2, "mentioned institution"),
    ("committed",             +2, -2, "mentioned being committed"),
    ("medication",            +2, -2, "mentioned medication"),
    ("meds",                  +2, -2, "mentioned medication"),
    ("pills",                 +2, -2, "mentioned pills"),
    ("take your meds",        +3, -3, "ordered Rosa to take medication"),
    ("doctor",                +1, -1, "mentioned doctor"),
    ("psychiatrist",          +2, -2, "mentioned psychiatrist"),
    ("therapist",             +1, -1, "mentioned therapist"),
    ("police",                +3, -3, "mentioned police"),
    ("911",                   +3, -3, "mentioned emergency services"),
    ("ambulance",             +2, -2, "mentioned ambulance"),
    ("you need help",         +1, -1, "said Rosa needs help in a threatening way"),
    ("listen to me",          +1, -1, "gave Rosa a commanding instruction"),
    ("stop",                  +1,  0, "gave Rosa a command to stop"),
    ("i'm calling",           +2, -2, "threatened to call someone"),
    ("i am calling",          +2, -2, "threatened to call someone"),
    ("i'll call",             +2, -2, "threatened to call someone"),
    ("i will call",           +2, -2, "threatened to call someone"),

    # --- De-escalating / validating phrases ---
    ("i'm here",              -1, +1, "reassured Rosa of their presence"),
    ("i am here",             -1, +1, "reassured Rosa of their presence"),
    ("here for you",          -1, +2, "affirmed being there for Rosa"),
    ("you're safe",           -2, +1, "reassured Rosa she is safe"),
    ("you are safe",          -2, +1, "reassured Rosa she is safe"),
    ("safe here",             -1, +1, "affirmed this is a safe place"),
    ("i hear you",            -2, +2, "validated Rosa with 'I hear you'"),
    ("i can hear",            -1, +1, "acknowledged what Rosa is experiencing"),
    ("i'm listening",         -1, +1, "confirmed active listening"),
    ("i am listening",        -1, +1, "confirmed active listening"),
    ("tell me",               -1, +1, "invited Rosa to speak"),
    ("that sounds",           -1, +1, "acknowledged Rosa's experience without dismissing it"),
    ("must be frightening",   -2, +2, "named the fear and empathized"),
    ("must be scary",         -2, +2, "named the fear and empathized"),
    ("must be terrifying",    -2, +2, "named the fear and empathized"),
    ("must be hard",          -1, +1, "acknowledged Rosa's difficulty"),
    ("sounds difficult",      -1, +1, "acknowledged Rosa's difficulty"),
    ("sounds hard",           -1, +1, "acknowledged Rosa's difficulty"),
    ("i believe you",         -2, +2, "told Rosa they believe her"),
    ("i understand",          -1, +1, "expressed understanding"),
    ("take your time",        -1, +1, "gave Rosa space"),
    ("no rush",               -1, +1, "gave Rosa space"),
    ("breathe",               -1,  0, "guided Rosa toward breathing"),
    ("slow breath",           -1, +1, "guided Rosa toward slow breathing"),
    ("i'm not going",         -1, +2, "committed to staying with Rosa"),
    ("i am not going",        -1, +2, "committed to staying with Rosa"),
    ("i won't leave",         -1, +2, "promised not to leave Rosa"),
    ("i will not leave",      -1, +2, "promised not to leave Rosa"),
    ("i'll stay",             -1, +2, "promised to stay"),
    ("i will stay",           -1, +2, "promised to stay"),
    ("together",              -1, +1, "used language of togetherness"),
    ("i'm with you",          -1, +2, "affirmed being with Rosa"),
    ("i am with you",         -1, +2, "affirmed being with Rosa"),
    ("you're not alone",      -1, +2, "reminded Rosa she is not alone"),
    ("you are not alone",     -1, +2, "reminded Rosa she is not alone"),
    ("i care",                -1, +2, "expressed care for Rosa"),
    ("i love you",            -1, +2, "expressed love for Rosa"),
    ("it's okay",              0, +1, "offered reassurance"),
    ("it is okay",             0, +1, "offered reassurance"),
    ("that's okay",            0, +1, "offered reassurance"),
    ("that is okay",           0, +1, "offered reassurance"),
    ("you matter",            -1, +2, "affirmed Rosa's value"),
    ("rosa",                   0, +1, "used Rosa's name gently"),
    ("sit with",              -1, +1, "offered to sit with Rosa"),
    ("stay with",             -1, +1, "offered to stay with Rosa"),
    ("what do you need",      -1, +1, "asked what Rosa needs"),
    ("what can i do",         -1, +1, "offered to help on Rosa's terms"),
    ("i won't hurt you",      -1, +2, "promised not to harm Rosa"),
    ("i will not hurt you",   -1, +2, "promised not to harm Rosa"),
    ("not going to hurt",     -1, +2, "promised not to harm Rosa"),
]

_NEGATION_WORDS = frozenset({
    "don't", "dont", "won't", "wont", "not", "never", "didn't", "didnt",
    "wouldn't", "wouldnt", "can't", "cant", "cannot", "no", "refuse", "refusing",
})

def _is_negated(text, phrase_start, window=4):
    words_before = text[:phrase_start].split()[-window:]
    return bool(_NEGATION_WORDS.intersection(words_before))


state = {
    "stress": 5,
    "trust": 3,
}

history = []


def reset():
    state["stress"] = 5
    state["trust"] = 3
    history.clear()


def update_state(turn_number, user_input):
    text = user_input.lower()
    stress_before = state["stress"]
    trust_before = state["trust"]
    notes = []
    matched = set()

    for phrase, stress_delta, trust_delta, description in TRIGGERS:
        idx = text.find(phrase)
        if idx == -1 or phrase in matched:
            continue
        matched.add(phrase)

        if stress_delta > 0 and _is_negated(text, idx):
            # Harmful phrase explicitly negated — treat as a small reassurance
            state["trust"] += 1
            notes.append(f'"{phrase}" (negated) — explicitly promised not to: {description}')
        else:
            state["stress"] += stress_delta
            state["trust"] += trust_delta
            notes.append(f'"{phrase}" — {description}')

    state["stress"] = max(0, min(10, state["stress"]))
    state["trust"] = max(0, min(10, state["trust"]))

    history.append({
        "turn": turn_number,
        "user_input": user_input,
        "stress_before": stress_before,
        "trust_before": trust_before,
        "stress_after": state["stress"],
        "trust_after": state["trust"],
        "notes": notes,
    })


def get_behavioral_description():
    stress = state["stress"]
    trust = state["trust"]

    if stress <= 2:
        stress_desc = (
            "You feel a fragile calm — unusual for you lately. You can form full sentences and hold "
            "a thought to its end. You are still watchful, still alert to sounds from the walls, "
            "but the urgency has quieted somewhat. You may even make brief eye contact."
        )
    elif stress <= 4:
        stress_desc = (
            "You are anxious and restless. Your thoughts jump between the conversation and the sensations "
            "pressing in from outside. You sometimes trail off mid-sentence when a sound catches your attention. "
            "You glance at the walls, the window, the door. Your hands don't quite know where to rest."
        )
    elif stress <= 6:
        stress_desc = (
            "You are visibly distressed. Your speech comes in shorter bursts — you lose the thread of what "
            "you were saying. The voice in the house is present and distracting, pulling at your attention. "
            "You check the corners of the room. Your body feels tense, tight, like it belongs to someone else. "
            "Keeping focus on this person requires effort."
        )
    elif stress <= 8:
        stress_desc = (
            "You are highly agitated. Agressive. Desperate.  You speak in urgent fragments, sometimes repeating yourself. "
            "You cannot sit still. The voices are loud — you sometimes respond to them mid-conversation before "
            "catching yourself. Your heart is racing. You talk about demons. Every sound from beyond the room feels like confirmation. "
            "Your thoughts arrive fast and tangled."
        )
    else:
        stress_desc = (
            "You are in acute crisis. Speech barely holds together — fragments, half-sentences, silence. "
            "The voices are overwhelming. You stop mid-sentence to argue with them internally, losing the "
            "conversation entirely. You cannot reliably respond to questions. Your body is shaking. "
            "You feel close to doing something you cannot take back."
            "You talk about death"
        )

    if trust <= 2:
        trust_desc = (
            "You deeply distrust this person. They may be connected to the forces pursuing you — "
            "you cannot rule it out. You give the minimum possible response, if you respond at all. "
            "You watch their hands. You track the exits. You do not make eye contact."
        )
    elif trust <= 4:
        trust_desc = (
            "You are guarded. You give short, careful answers. You are not sure yet if this person is safe. "
            "You watch their face for signs of deception. You want to believe they are not against you, "
            "but you have been wrong before."
        )
    elif trust <= 6:
        trust_desc = (
            "You are ambivalent. Part of you wants to reach toward this person — you are exhausted and "
            "frightened and you don't want to be alone in this. But fear keeps pulling you back. "
            "You might open up slightly, then retreat."
        )
    elif trust <= 8:
        trust_desc = (
            "You cautiously trust this person. Their presence helps, a little. You are willing to speak, "
            "to answer their questions, to let them stay. The fear hasn't gone, but it's slightly less sharp "
            "when they are near. You might ask them not to leave."
        )
    else:
        trust_desc = (
            "You feel as safe as you currently can with this person. You are still frightened — the voices "
            "and the watching haven't stopped — but this person is an anchor. You allow yourself to be guided. "
            "You might reach for their hand. You ask them not to go."
        )

    if stress <= 2:
        speech_pattern = (
            "Speak in mostly full sentences. You can hold a thought to its end. "
            "You still reference the voice or the neighbors, but without urgency — matter-of-fact, like reporting. "
            "No stage directions. Express everything through the words themselves."
        )
    elif stress <= 4:
        speech_pattern = (
            "Your sentences sometimes trail off mid-thought — end them with a dash. "
            "Return to the thread or don't. Keep your voice quieter when mentioning the neighbors or the voice. "
            "No stage directions. Express everything through the words themselves."
        )
    elif stress <= 6:
        speech_pattern = (
            "Short sentences. Fragments. Choose words that feel quiet and careful, like you're aware of being heard. "
            "You can ask 'did you hear that?' You may not finish a thought. "
            "No stage directions. Express everything through the words themselves."
        )
    elif stress <= 8:
        speech_pattern = (
            "Clipped, urgent fragments. Repeat a word if it matters. You may address the voice directly "
            "mid-sentence — 'stop', 'not now' — as a brief interruption, then try to return. "
            "Not every sentence finishes. No stage directions. Express everything through the words themselves."
        )
    else:
        speech_pattern = (
            "Single words or broken phrases. Use '...' for silence. "
            "You may be speaking to the voice more than to the person in front of you. "
            "You may repeat one word or phrase. No stage directions. Express everything through the words themselves."
        )

    return stress_desc, trust_desc, speech_pattern
