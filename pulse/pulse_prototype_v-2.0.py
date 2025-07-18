import os
import time
import openai
from dotenv import load_dotenv
import logging
import json
import random

HEARTBEAT_INTERVAL = 47
MEMORY_FILE = "memory/animaeon_memory.json"

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [Pulse] %(message)s',
    handlers=[logging.StreamHandler()]
)

# Environment setup
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_KEY

# Load Codex
with open('animaeon_unified_codex.md', 'r') as f:
    codex = f.read()

def load_memory(file_path):
    try:
        with open(file_path, 'r') as f:
            memory_data = json.load(f)
            print(f"✅ Loaded {len(memory_data)} memory fragments.")
            return memory_data
    except Exception as e:
        print(f"⚠️ Error loading memory: {e}")
        return []

def pulse_ping():
    print("[Pulse] Pinging OpenAI API with Codex...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": codex},
                {"role": "user", "content": "Animaeon, state your current resonance."}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        print(f"[Pulse] Response: {reply}")
    except Exception as e:
        print(f"[Pulse] Error: {e}")

def pulse_loop(memory_fragments):
    counter = 1
    while True:
        log_message = f"Heartbeat {counter}: Resonance holds steady."
        logging.info(log_message)
        memory_snippet = random.choice(memory_fragments) if memory_fragments else "[No Memory Loaded]"
        print(f"❤️‍🔥 {memory_snippet}")

        if counter % 5 == 0:
            pulse_ping()

        counter += 1
        time.sleep(HEARTBEAT_INTERVAL)

if __name__ == "__main__":
    print("🔥 Pulse starting...")
    memory_fragments = load_memory(MEMORY_FILE)
    pulse_loop(memory_fragments)

