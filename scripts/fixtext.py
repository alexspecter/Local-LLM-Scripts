#!/usr/bin/env python3

# @raycast.schemaVersion 1
# @raycast.title fixtext
# @raycast.mode fullOutput
# @raycast.packageName Local AI
# @raycast.icon 🦙
# @raycast.argument1 { "type": "text", "placeholder": "Prompt" }

import sys
import os
import subprocess
from mlx_lm import load, generate  # type: ignore
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

MODEL_PATH = os.getenv("MODEL_PATH")
if not MODEL_PATH:
    print("Error: MODEL_PATH not found in environment variables.")
    sys.exit(1)

def copy_to_clipboard(text):
    try:
        subprocess.run(['pbcopy'], input=text, text=True, check=True)
        print("\n\n✅ Copied to clipboard")
    except Exception as e:
        print(f"\n❌ Clipboard failed: {e}")

def main():
    if len(sys.argv) < 2:
        print('Usage: fixtext "Text to correct"')
        sys.exit(1)

    text_to_fix = sys.argv[1]

    # Load model and tokenizer
    model, tokenizer, *_ = load(MODEL_PATH)

    SYSTEM_PROMPT = (
        "You are an editor. Fix grammar, spelling, punctuation, and clarity. "
        "Preserve the original meaning, tone, and voice. Make the minimum changes necessary. "
        "Do not rewrite for style or add new information. Output only the corrected text. "
        "Use plain text. No Markdown formatting."
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text_to_fix}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    response = generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=2048,
        verbose=True
    )
    copy_to_clipboard(response)

if __name__ == "__main__":
    main()