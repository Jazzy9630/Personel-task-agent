"""
The agent's toolbox.

Each tool is two things:
  1. A SCHEMA -> what the model sees (name, description, parameters).
  2. A FUNCTION -> the real code that runs when the model asks for that tool.

The schemas use the OpenAI-style function shape.
"""

import os
import datetime
from groq import Groq
from dotenv import load_dotenv

import config

load_dotenv()

# Groq client reads GROQ_API_KEY from .env automatically.
_client = Groq()


# ---------------------------------------------------------------------------
# TOOL 1 — research
# ---------------------------------------------------------------------------

research_schema = {
    "type": "function",
    "function": {
        "name": "research",
        "description": (
            "Research a topic and return a short, factual set of notes about it. "
            "Use this when you need information before writing anything."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The subject to research, e.g. 'the James Webb telescope'.",
                }
            },
            "required": ["topic"],
        },
    },
}


def research(topic: str) -> str:
    """
    Research a topic and return structured, useful notes.
    """

    prompt = f"""
Create detailed but concise research notes about: {topic}.

Use this format:

# {topic}

## Overview
Explain what the topic is.

## Key Facts
Provide important facts and background information.

## Main Applications
Explain where this topic is used.

## Benefits
List the advantages.

## Challenges
List limitations or problems.

## Conclusion
Give a short summary.

Rules:
- Use bullet points where useful.
- Keep information factual and easy to understand.
- Do not write an introduction.
- Return only the research notes.
"""

    resp = _client.chat.completions.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return resp.choices[0].message.content


# ---------------------------------------------------------------------------
# TOOL 2 — save_note
# ---------------------------------------------------------------------------

save_note_schema = {
    "type": "function",
    "function": {
        "name": "save_note",
        "description": (
            "Save text to a note file so it can be reused later. "
            "Use this to store research findings before writing a summary."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "File name only, e.g. 'webb-notes.md'. No folders.",
                },
                "content": {
                    "type": "string",
                    "description": "The text to save.",
                },
            },
            "required": ["filename", "content"],
        },
    },
}


def save_note(filename: str, content: str) -> str:
    """Write content to notes/<filename>."""

    os.makedirs(config.NOTES_DIR, exist_ok=True)

    safe_name = os.path.basename(filename)
    path = os.path.join(config.NOTES_DIR, safe_name)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"Saved {len(content)} characters to {path}"


# ---------------------------------------------------------------------------
# TOOL 3 — send_email
# ---------------------------------------------------------------------------

send_email_schema = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": (
            "Send a clean and professional email summary to a recipient. "
            "Use this as the final step after research and note creation. "
            "The email body should summarize important findings."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient email address."
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line."
                },
                "body": {
                    "type": "string",
                    "description": "Full email body."
                },
            },
            "required": ["to", "subject", "body"],
        },
    },
}


def send_email(to: str, subject: str, body: str) -> str:
    """
    Dry-run email. Does not actually send.
    Approval gate protects this tool.
    """

    when = datetime.datetime.now().strftime("%H:%M:%S")

    print("\n----- DRY-RUN EMAIL -------------------------------")
    print(f"time:    {when}")
    print(f"from:    Jahanzaib Muhammad Talib <Jahanzebsiyal4@outlook.com>")
    print(f"to:      {to}")
    print(f"subject: {subject}")
    print("body:")
    print(body)
    print("---------------------------------------------------\n")

    return f"(dry-run) email to {to} prepared but not actually sent"


# ---------------------------------------------------------------------------
# Registries
# ---------------------------------------------------------------------------

TOOL_SCHEMAS = [
    research_schema,
    save_note_schema,
    send_email_schema
]


TOOL_FUNCTIONS = {
    "research": research,
    "save_note": save_note,
    "send_email": send_email,
}