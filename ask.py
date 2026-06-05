#!/usr/bin/env python3

# @raycast.schemaVersion 1
# @raycast.title ask
# @raycast.mode fullOutput
# @raycast.packageName Local AI
# @raycast.icon 🦙
# @raycast.argument1 { "type": "text", "placeholder": "Prompt" }

import sys
import os
from mlx_lm import load, generate  # type: ignore
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
if not MODEL_PATH:
    print("Error: MODEL_PATH not found in environment variables.")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print('Usage: ask "Your prompt here"')
        sys.exit(1)

    user_prompt = sys.argv[1]

    model, tokenizer, *_ = load(MODEL_PATH)

    SYSTEM_PROMPT = "Respond in plain text only. Do not use Markdown, bullet points, or formatting characters."
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=4096,
        verbose=True
    )

if __name__ == "__main__":
    main()
