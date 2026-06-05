#!/usr/bin/env python3

# @raycast.schemaVersion 1
# @raycast.title fixprompt
# @raycast.mode fullOutput
# @raycast.packageName Local AI
# @raycast.icon 🦙
# @raycast.argument1 { "type": "text", "placeholder": "Prompt to optimize" }

import sys
import os
import subprocess
import re
from mlx_lm import load, generate  # type: ignore
from dotenv import load_dotenv
load_dotenv()


MODEL_PATH = os.getenv("MODEL_PATH")
if not MODEL_PATH:
    print("Error: MODEL_PATH not found in environment variables.")
    sys.exit(1)
script_dir = os.path.dirname(os.path.abspath(__file__))
Prompt_folder = os.path.join(script_dir, "System Prompts")
system_prompt_location = os.path.join(Prompt_folder, "fixprompt.md")

# Read system prompt safely
try:
    with open(system_prompt_location, "r", encoding="utf-8") as f:
        system_prompt_file = f.read()
except FileNotFoundError:
    print("Error: System prompt file not found.")
    sys.exit(1)

def parse_output(text):
    """Extracts content inside the first markdown code block ``` ... ```."""
    # Regex searches for ``` followed by optional language name, then content, then ```
    match = re.search(r"```(?:\w+)?\s*(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text # Fallback: return original if no code block found

def copy_to_clipboard(text):
    try:
        subprocess.run(['pbcopy'], input=text, text=True, check=True)
        print("\n\n✅ Optimized prompt copied to clipboard")
    except Exception as e:
        print(f"\n❌ Clipboard failed: {e}")

def main():
    if len(sys.argv) < 2:
        print('Usage: fixprompt "Prompt to optimize"')
        sys.exit(1)

    text_to_fix = sys.argv[1]

    # Load model and tokenizer
    model, tokenizer, *_ = load(MODEL_PATH)

    SYSTEM_PROMPT = system_prompt_file

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text_to_fix}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    # Capture response
    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=2048,
        verbose=True
    )
    
    # Parse and Copy
    clean_text = parse_output(response)
    copy_to_clipboard(clean_text)

if __name__ == "__main__":
    main()