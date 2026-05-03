import readline
import random
import sys
import tty
import termios
import atexit
import subprocess
import threading
import array
import math
import time
import ollama

MAGENTA = "\033[1;35m"
RESET  = "\033[0m"
from scenario import SCENARIO
from state import state, update_state, reset, get_behavioral_description, get_dominant_symptom, history, SYMPTOMS

# USAGE:
# python rosa_bot.py          -> uses qwen (default, stable)
# python rosa_bot.py gemma    -> uses gemma2:9b (test)

MODEL_MAP = {
    "qwen": "rosa",       # Qwen 2.5 7B (current stable)
    "gemma": "gemma2:9b"  # Gemma2 9B (test)
}

PIPER_BIN   = "/home/kadaver/Documents/you-after/venv/bin/piper"
VOICE_MODEL = "/home/kadaver/Documents/you-after/voice/en_US-amy-medium.onnx"
VOICE_SPEED = 0.87  # length_scale: lower = faster (0.5 very fast · 1.0 normal · 1.5 slow)

_piper_proc = None
_aplay_proc = None

def _stop_audio():
    global _piper_proc, _aplay_proc
    for p in (_piper_proc, _aplay_proc):
        if p:
            try: p.kill()
            except: pass
    _piper_proc = _aplay_proc = None

def _gen_ring():
    """One ring cycle: 1s dual-tone (440+480 Hz) + 2s silence."""
    buf = array.array('h')
    for i in range(22050):
        t = i / 22050
        v = 0.35 * math.sin(2 * math.pi * 440 * t) + 0.35 * math.sin(2 * math.pi * 480 * t)
        buf.append(int(v * 32767))
    buf.extend([0] * (22050 * 2))
    return buf.tobytes()

def _gen_click():
    """Short pickup click (~20ms sharp transient)."""
    buf = array.array('h')
    n = int(22050 * 0.02)
    for i in range(n):
        decay = 1.0 - (i / n) ** 0.5
        v = decay * (0.9 if i % 2 == 0 else -0.9)
        buf.append(int(v * 32767))
    return buf.tobytes()

def _ring_loop(stop_event):
    ring = _gen_ring()
    chunk = 22050 // 10 * 2  # 0.1s of bytes
    proc = subprocess.Popen(
        ['aplay', '-r', '22050', '-f', 'S16_LE', '-t', 'raw', '-q', '-'],
        stdin=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    try:
        pos = 0
        while not stop_event.is_set():
            end = pos + chunk
            if end >= len(ring):
                proc.stdin.write(ring[pos:])
                proc.stdin.flush()
                pos = 0
            else:
                proc.stdin.write(ring[pos:end])
                proc.stdin.flush()
                pos = end
    except BrokenPipeError:
        pass
    finally:
        try: proc.kill()
        except: pass
        proc.wait()

def _play_click():
    proc = subprocess.Popen(
        ['paplay', '/usr/share/sounds/freedesktop/stereo/camera-shutter.oga'],
        stderr=subprocess.DEVNULL
    )
    proc.wait()

def speak(text):
    def _run():
        global _piper_proc, _aplay_proc
        _stop_audio()
        _piper_proc = subprocess.Popen(
            [PIPER_BIN, "--model", VOICE_MODEL, "--output-raw"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        _aplay_proc = subprocess.Popen(
            ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw", "-q", "-"],
            stdin=_piper_proc.stdout, stderr=subprocess.DEVNULL
        )
        _piper_proc.stdin.write(text.encode())
        _piper_proc.stdin.close()
        _piper_proc.stdout.close()
        _aplay_proc.wait()
        _piper_proc = _aplay_proc = None
    threading.Thread(target=_run, daemon=True).start()

def speak_synced(text):
    """Generate audio first, then play it and print text as typewriter in sync."""
    global _piper_proc, _aplay_proc
    _stop_audio()

    piper = subprocess.Popen(
        [PIPER_BIN, "--model", VOICE_MODEL, "--output-raw", "--length_scale", str(VOICE_SPEED)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )
    audio_data, _ = piper.communicate(text.encode())

    if not audio_data:
        sys.stdout.write(text)
        sys.stdout.flush()
        return

    duration = len(audio_data) / (22050 * 2)
    char_delay = duration / max(len(text), 1)

    _aplay_proc = subprocess.Popen(
        ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw", "-q", "-"],
        stdin=subprocess.PIPE, stderr=subprocess.DEVNULL
    )

    def _play():
        global _aplay_proc
        _aplay_proc.stdin.write(audio_data)
        _aplay_proc.stdin.close()
        _aplay_proc.wait()
        _aplay_proc = None

    audio_thread = threading.Thread(target=_play, daemon=True)
    audio_thread.start()

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(char_delay)

    audio_thread.join()

selected = sys.argv[1] if len(sys.argv) > 1 else "qwen"
MODEL = MODEL_MAP.get(selected, "rosa")

print(f"\n[Using model: {MODEL}]\n")

reset()

print("=" * 55)
print("  ROSA SIMULATOR")
print("  Practice communicating with someone in crisis.")
print("  Type 'exit' to end the session.")
print("=" * 55)
print()
print("  [1] In-person meeting")
print("  [2] Phone call  (Rosa called you)")
print("  [CTRL+v] Rosa's voice on/off ")
print("  [Enter] Random")
print()

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
atexit.register(termios.tcsetattr, fd, termios.TCSADRAIN, old_settings)
atexit.register(_stop_audio)
try:
    tty.setraw(fd)
    mode_choice = sys.stdin.read(1)
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()

if mode_choice == "1":
    mode = "meeting"
elif mode_choice == "2":
    mode = "phone"
else:
    mode = random.choice(["meeting", "phone"])
    label = "In-person meeting" if mode == "meeting" else "Phone call"
    print(f"  → Random: {label}")

print()

voice_on = (mode == "phone")
if mode == "phone":
    readline.parse_and_bind(r'"\C-v": "\C-a\C-kVOICE_TOGGLE\n"')

PHONE_TRIGGERS = [
    "She called because a voice told her someone was coming for her.",
    "She called because she heard knocking inside the walls and it won't stop.",
    "She called because the TV started sending her a message meant only for her.",
    "She called because she saw something move in the corner and she can't look away.",
    "She called because she's afraid to go to the kitchen and doesn't know what to do.",
    "She called because she hasn't slept and something is getting closer.",
]

MEETING_TRIGGERS = [
    "She was covering the devices when the person arrived.",
    "She heard knocking and opened the door, not sure if it was a neighbor or something else.",
    "She was praying when the person walked in — and praying made it worse.",
    "She saw a shadow move near the window just before the person appeared.",
    "She was standing very still, listening through the walls, when the person arrived.",
]

if mode == "meeting":
    mode_context = "You are face to face with someone who just arrived at your home. You don't know who they are."
    trigger = random.choice(MEETING_TRIGGERS)
    opening_prompt = f"{SCENARIO}\n\n{trigger} Write Rosa's first words to this person. 1 to 2 sentences. Suspicious and frightened. First person only."
else:
    state["stress"] = 7
    mode_context = "You called someone on the phone. You cannot see them. You are desperate and need help."
    trigger = random.choice(PHONE_TRIGGERS)
    opening_prompt = f"{SCENARIO}\n\n{trigger} The call was just answered. Write Rosa's first words. 1 to 2 sentences. First person only."

label = "[ IN PERSON ]" if mode == "meeting" else "[ PHONE CALL ]"
print(f"  {label}")
print("-" * 55)

if mode == "phone":
    _ring_stop = threading.Event()
    _ring_thread = threading.Thread(target=_ring_loop, args=(_ring_stop,), daemon=True)
    _ring_thread.start()

opening_response = ollama.generate(
    model=MODEL,
    prompt=opening_prompt,
    options={"temperature": 0.9, "seed": random.randint(1, 99999), "num_predict": 80, "stop": ["YOU:", "ROSA:", "\n", "*", "("]}
)
opening = opening_response["response"].strip().replace('"', '')
if mode == "phone":
    _ring_stop.set()
    _ring_thread.join(timeout=0.3)
    _play_click()
    sys.stdout.write(f"\n{MAGENTA}ROSA:{RESET} ")
    sys.stdout.flush()
    speak_synced(opening)
    sys.stdout.write(f"\n{MAGENTA}[voice on]{RESET}\n\n")
    sys.stdout.flush()
else:
    print(f"\n{MAGENTA}ROSA:{RESET} {opening}\n")

conversation_lines = [f"ROSA: {opening}"]
turn = 0

while True:
    user_input = input("YOU: ").strip()

    if not user_input:
        continue
    if user_input.lower() == "exit":
        break

    if user_input == "VOICE_TOGGLE":
        sys.stdout.write('\033[1A\033[2K\r')
        sys.stdout.flush()
        voice_on = not voice_on
        if not voice_on:
            _stop_audio()
        status = "on" if voice_on else "off"
        print(f"{MAGENTA}[voice {status}]{RESET}\n")
        continue

    turn += 1
    update_state(turn, user_input, mode)
    stress_desc, trust_desc = get_behavioral_description(mode)
    dominant_symptom = get_dominant_symptom()

    second_symptom = random.choice([s for s in SYMPTOMS if s != dominant_symptom])

    if mode == "meeting" and state["stress"] > 7:
        symptom_line = f"The world fragments: {dominant_symptom}. {second_symptom} is bleeding into everything."
        turn_temp = 1.2
        repeat_pen = 1.1
        top_p = 0.95
    else:
        symptom_line = f"Right now she notices: {dominant_symptom}"
        turn_temp = 0.8 
        repeat_pen = 1.1
        top_p = 0.90

    recent_history = "\n".join(conversation_lines[-8:]) if conversation_lines else "Beginning of conversation."

    prompt = f"""
{SCENARIO}

Context: {mode_context}
Rosa feels: {stress_desc} {trust_desc}
{symptom_line}

Recent Conversation:
{recent_history}

The person says: "{user_input}"

Respond as Rosa. Use a mix of long, rambling sentences and short, panicked ones. 
Aim for 3-6 sentences. First person only. No narration.

ROSA:"""

    response = ollama.generate(
        model=MODEL,
        prompt=prompt,
        options={
            "temperature": turn_temp,
            "repeat_penalty": repeat_pen,
            "top_p": top_p,
            "num_predict": 100,
            "stop": ["YOU:", "ROSA:", "\n\n", "*"]
        }
    )

    reply = response["response"].strip().replace('"', '')

    if mode == "phone" and voice_on:
        sys.stdout.write(f"\n{MAGENTA}ROSA:{RESET} ")
        sys.stdout.flush()
        speak_synced(reply)
        sys.stdout.write("\n\n")
        sys.stdout.flush()
    else:
        print(f"\n{MAGENTA}ROSA:{RESET} {reply}\n")

    conversation_lines.append(f"YOU: {user_input}")
    conversation_lines.append(f"ROSA: {reply}")

    if mode == "phone" and "hospital" in user_input.lower() and state["trust"] <= 2:
        print(f"{MAGENTA}ROSA:{RESET} [call disconnected]\n")
        break

    if mode == "phone" and ("police" in user_input.lower() or "jail" in user_input.lower()):
        print(f"{MAGENTA}ROSA:{RESET} [call disconnected]\n")
        break

    if mode == "phone" and state["stress"] >= 10 and state["trust"] <= 0:
        print(f"{MAGENTA}ROSA:{RESET} [call disconnected]\n")
        break

    if mode == "meeting" and "hospital" in user_input.lower() and state["trust"] <= 2:
        print(f"{MAGENTA}ROSA:{RESET} [Rosa runs]\n")
        break

    if mode == "meeting" and ("police" in user_input.lower() or "jail" in user_input.lower()):
        print(f"{MAGENTA}ROSA:{RESET} [Rosa runs]\n")
        break

    if mode == "meeting" and state["stress"] >= 10 and state["trust"] <= 0:
        print(f"{MAGENTA}ROSA:{RESET} [Rosa runs]\n")
        break

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
        notes = "; ".join(entry["notes"]) if entry["notes"] else "neutral interaction"
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
        print(f"  → Rosa's distress decreased.")
    elif stress_delta == 0:
        print("  → Rosa's distress was unchanged.")
    else:
        print(f"  → Rosa's distress INCREASED — review what escalated her.")

    if trust_delta > 2:
        print("  → Rosa's trust SIGNIFICANTLY INCREASED — she felt safe with you.")
    elif trust_delta > 0:
        print(f"  → Rosa's trust increased.")
    elif trust_delta == 0:
        print("  → Rosa's trust was unchanged.")
    else:
        print(f"  → Rosa's trust DECREASED — she felt less safe with you.")

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
