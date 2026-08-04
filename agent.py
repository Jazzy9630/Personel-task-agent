"""
Personal Task Agent — Groq version.

Uses:
- Groq API (fast open-weight models)
- OpenAI-compatible chat completion format
- Tool calling
- Approval gate
- Logging
- Iteration limit
"""

import sys
import os
import json
import datetime

from groq import Groq, BadRequestError
from dotenv import load_dotenv

import config
from tools import TOOL_SCHEMAS, TOOL_FUNCTIONS


# Load .env
load_dotenv()


# Groq client — picks up GROQ_API_KEY from the environment automatically.
client = Groq()


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

def _log_path():
    os.makedirs(config.LOG_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return os.path.join(config.LOG_DIR, f"run-{stamp}.log")


LOG_FILE = _log_path()


def log(line):
    stamp = datetime.datetime.now().strftime("%H:%M:%S")
    entry = f"{stamp}  {line}"

    print(entry)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


# ---------------------------------------------------------
# Approval system
# ---------------------------------------------------------

def needs_approval(tool_name):
    return tool_name not in config.AUTO_APPROVE



def ask_human(tool_name, tool_input):

    print("\n>>> APPROVAL NEEDED")
    print(f"tool: {tool_name}")

    for key, value in tool_input.items():
        preview = str(value)

        if len(preview) > 300:
            preview = preview[:300] + "..."

        print(f"{key}: {preview}")


    answer = input(
        ">>> Approve this action? (y/n): "
    ).lower().strip()

    return answer == "y"



# ---------------------------------------------------------
# Tool execution
# ---------------------------------------------------------

def run_tool(tool_name, tool_input):

    if needs_approval(tool_name):

        if not ask_human(tool_name, tool_input):

            log(
                f"DENIED {tool_name}"
            )

            return (
                "Human rejected this action."
            )


        log(
            f"APPROVED {tool_name}"
        )


    func = TOOL_FUNCTIONS.get(tool_name)


    if func is None:

        log(
            f"ERROR unknown tool {tool_name}"
        )

        return (
            f"Tool {tool_name} does not exist."
        )


    log(
        f"CALL {tool_name} {tool_input}"
    )


    try:

        result = func(**tool_input)


    except Exception as exc:

        log(
            f"ERROR {tool_name}: {exc}"
        )

        return (
            f"Tool failed: {exc}"
        )


    log(
        f"RESULT {str(result)[:200]}"
    )


    return str(result)



# ---------------------------------------------------------
# Message helpers
# ---------------------------------------------------------

def tool_result_block(tool_call_id, content):

    return {

        "role": "tool",

        "tool_call_id": tool_call_id,

        "content": content

    }



def assistant_block(message):

    block = {

        "role": "assistant",

        "content": message.content or ""

    }


    if message.tool_calls:

        block["tool_calls"] = []


        for call in message.tool_calls:

            block["tool_calls"].append({

                "id": call.id,

                "type": "function",

                "function": {

                    "name": call.function.name,

                    "arguments": call.function.arguments

                }

            })


    return block



# ---------------------------------------------------------
# Main Agent Loop
# ---------------------------------------------------------

def run(goal):

    log(
        f"GOAL {goal}"
    )


    messages = [

        {
            "role": "user",
            "content": goal
        }

    ]


    for turn in range(
        1,
        config.MAX_ITERATIONS + 1
    ):


        log(
            f"--- turn {turn}/{config.MAX_ITERATIONS} ---"
        )


        try:

            response = client.chat.completions.create(

                model=config.MODEL,

                max_tokens=config.MAX_TOKENS,

                tools=TOOL_SCHEMAS,

                messages=messages

            )


        except BadRequestError as exc:


            log(
                f"API ERROR {exc}"
            )


            messages.append({

                "role": "user",

                "content":
                "Your tool call was invalid. Retry with valid JSON."

            })


            continue



        if not response.choices:

            log(
                "ERROR no response choices"
            )

            messages.append({

                "role":"user",

                "content":
                "Try again."

            })

            continue



        message = response.choices[0].message


        messages.append(
            assistant_block(message)
        )



        # Finished

        if not message.tool_calls:


            log(
                "DONE"
            )


            print(
                "\n=== FINAL ANSWER ==="
            )


            print(
                message.content or ""
            )


            return




        # Execute tools

        for call in message.tool_calls:


            try:

                tool_input = json.loads(
                    call.function.arguments or "{}"
                )


            except json.JSONDecodeError as exc:


                log(
                    f"BAD JSON {exc}"
                )


                messages.append(

                    tool_result_block(

                        call.id,

                        "Invalid JSON arguments."

                    )

                )


                continue



            result = run_tool(

                call.function.name,

                tool_input

            )


            messages.append(

                tool_result_block(

                    call.id,

                    result

                )

            )



    log(
        "STOPPED iteration limit"
    )


    print(
        "\n=== STOPPED ==="
    )



# ---------------------------------------------------------
# Entry
# ---------------------------------------------------------

if __name__ == "__main__":


    if len(sys.argv) < 2:


        print(
            'Usage: python agent.py "your task"'
        )

        sys.exit(1)



    run(
        " ".join(sys.argv[1:])
    )