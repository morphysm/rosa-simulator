# Rosa Simulator

A conversational simulator to help health professionals and family members practice communicating with someone in a pre-psychotic or schizophrenic crisis.

Rosa is alone at home at night experiencing a crisis that feels completely real to her. The goal is not to "fix" her. The goal is to learn how to be present with her.

---

## Who it's for

- Mental health professionals in training
- Nurses, social workers, first responders
- Family members of people with psychotic disorders
- Anyone who wants to understand what it feels like to communicate across that distance

---

## How it works

You talk to Rosa. She responds based on her inner world — her fears, her beliefs, what she hears and sees. Her state changes depending on how you speak to her.

Two values track the conversation beneath the surface:

- **Stress (0–10)** — her level of distress and agitation
- **Trust (0–10)** — how safe she feels with you

Certain phrases escalate her. Others help. At the end of each session, a debrief shows you exactly what happened — turn by turn — and what you said that mattered.

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally
- A model named `rosa` loaded in Ollama

---

## Setup

```bash
git clone https://github.com/morphysm/rosa-simulator.git
cd rosa-simulator
python3 -m venv env
source env/bin/activate
pip install ollama
```

You will need to create and load your own `rosa` model in Ollama. The character and behavior are defined in `scenario.py`.

---

## Run

```bash
python3 rosa_bot.py
```

Or, if you set up the shell shortcut:

```bash
rosa-bot
```

Type `exit` to end the session and see the debrief.

---

## Files

| File | Purpose |
| --- | --- |
| `scenario.py` | Rosa's inner world — her beliefs, fears, and sensory experience |
| `state.py` | Stress/trust state engine, trigger phrases, session history |
| `rosa_bot.py` | Main loop, prompt builder, session debrief |

---

## What the debrief shows

At the end of each session you see:

- Turn-by-turn stress and trust changes
- Which specific phrases triggered each change
- Your best and hardest moments
- An overall outcome: did Rosa feel safer or more afraid by the end?

---

## A note on the scenario

Rosa's inner world is based on clinical descriptions of pre-psychotic and first-episode psychotic states. She experiences command hallucinations, paranoid ideation, depersonalization, and visual hypervigilance. She is not confused — she is terrified of what she believes reality contains.

The simulator is designed to teach presence, validation, and de-escalation — not diagnosis or correction.

---

*Built with [Ollama](https://ollama.com) and Python.*
