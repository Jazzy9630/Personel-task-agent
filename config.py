"""
Central knobs for the agent. Change behaviour here, not scattered through the code.
"""

# Model provider
# This project uses Groq's OpenAI-compatible chat completions API.
#
# Groq retires model names periodically — if a run fails with
# `model_not_found`, this is the line to update.
# Must be a strong tool-caller; see CLAUDE.md for why.

MODEL = "openai/gpt-oss-120b"


# Safety limit.
# The agent stops after this many turns.
MAX_ITERATIONS = 8


# Maximum response length from the model.
MAX_TOKENS = 4096


# Tools allowed without asking permission.
# Reading and saving notes are safe.
# Sending email requires approval.

AUTO_APPROVE = {
    "research",
    "save_note",
}


# Folder locations.

NOTES_DIR = "notes"
LOG_DIR = "logs"