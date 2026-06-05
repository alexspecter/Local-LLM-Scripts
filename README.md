# AI Scripts

A collection of local LLM-powered productivity tools that run as [Raycast](https://www.raycast.com/) commands. All inference runs on-device via [MLX](https://github.com/ml-explore/mlx) — no API keys, no data leaving your machine.

**Requires Apple Silicon (M1 or later).**

---

## Scripts

| Script | Raycast Command | What it does |
|---|---|---|
| `ask.py` | `ask` | General-purpose Q&A — plain text answers, no Markdown |
| `fixtext.py` | `fixtext` | Fixes grammar, spelling, and clarity while preserving your voice |
| `fixmessage.py` | `fixmessage` | Rewrites a work message to be clearer and more professional |
| `fixprompt.py` | `fixprompt` | Optimizes a rough prompt into a structured LLM prompt |

`fixtext`, `fixmessage`, and `fixprompt` automatically copy the result to your clipboard.

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/alexspecter/ai-scripts
cd ai-scripts
uv sync
```

> Requires [uv](https://github.com/astral-sh/uv). Install with `brew install uv` or `pip install uv`.

### 2. Configure your model

```bash
cp .env.example .env
```

Edit `.env` and set `MODEL_PATH` to any MLX-compatible model from [Hugging Face](https://huggingface.co/mlx-community):

```
MODEL_PATH=mlx-community/Qwen2.5-32B-Instruct-4bit
```

The model will be downloaded automatically on first run. A 4-bit quantized 32B model requires ~20GB of RAM.

### 3. Add scripts to Raycast

1. Open Raycast → Settings → Extensions → Script Commands
2. Add a new script directory pointing to this repo
3. The scripts will appear as commands in Raycast

---

## Dependencies

- [mlx-lm](https://github.com/ml-explore/mlx-lm) — local LLM inference on Apple Silicon
- [promptloop](https://github.com/alexspecter/promptloop) — prompt utilities
- [python-dotenv](https://github.com/theskumar/python-dotenv) — `.env` config loading
