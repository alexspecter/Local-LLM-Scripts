#!/usr/bin/env python3

# @raycast.schemaVersion 1
# @raycast.title fixmessage
# @raycast.mode fullOutput
# @raycast.packageName Local AI
# @raycast.icon 🦙
# @raycast.argument1 { "type": "text", "placeholder": "Message to fix" }

import sys
import os
import subprocess
from dotenv import load_dotenv
from mlx_lm import load, generate  # type: ignore

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
if not MODEL_PATH:
    print("Error: MODEL_PATH not found in environment variables.")
    sys.exit(1)
script_dir = os.path.dirname(os.path.abspath(__file__))
Prompt_folder = os.path.join(script_dir, "System Prompts")
system_prompt_location = os.path.join(Prompt_folder, "fixmessage.md")

# Read system prompt safely
try:
    with open(system_prompt_location, "r", encoding="utf-8") as f:
        system_prompt_file = f.read()
except FileNotFoundError:
    print("Error: System prompt file not found.")
    sys.exit(1)

def parse_output(text):
    """Extracts text between '### Revised Message' and '### Diagnostic Feedback'."""
    try:
        # Check if the expected header exists
        if "### Revised Message" in text:
            # Take everything AFTER "### Revised Message"
            content = text.split("### Revised Message")[1]
            
            # If the second header exists, take everything BEFORE it
            if "### Diagnostic Feedback" in content:
                content = content.split("### Diagnostic Feedback")[0]
            
            return content.strip()
    except Exception:
        pass # If parsing fails, return original text safely
    
    return text

def copy_to_clipboard(text):
    try:
        subprocess.run(['pbcopy'], input=text, text=True, check=True)
        print("\n\n✅ Revised message copied to clipboard")
    except Exception as e:
        print(f"\n❌ Clipboard failed: {e}")

def main():
    if len(sys.argv) < 2:
        print('Usage: fixmessage "Message to fix"')
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