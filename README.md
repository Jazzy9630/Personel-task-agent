# 🤖 Personal Task Agent

An AI-powered personal assistant that completes real-world multi-step tasks from a single command.

The agent can research information, generate structured notes, save files, and prepare email summaries while maintaining safety through human approval, logging, and execution limits.

# 📌 Project Overview

Personal Task Agent is an autonomous AI agent built using Python and an OpenAI-compatible API.

The agent follows a:

Reason → Act → Observe

workflow.

Instead of manually completing every step, the user provides one natural language command and the agent decides which tools to use to complete the task.

### Example:

python agent.py "Research black holes, save notes to blackholes.md, then email a summary to Jahanzebsiyal4@outlook.com"


The agent automatically performs:

1. Research the requested topic
2. Generate structured information
3. Save notes into a Markdown file
4. Ask for human approval before email action
5. Prepare the email summary
6. Record the complete execution log


# ✨ Features

## 🔍 AI Research

The agent can analyze a given topic and generate structured research notes.

Example:

Research black holes


Output includes:

1. Overview
2. Key facts
3. Applications
4. Benefits
5. Challenges
6. Conclusion



## 📝 Automatic Note Saving

Research results are automatically saved as Markdown files.

Example:

notes/
└── blackholes.md


## 📧 Email Summary Generation

The agent can prepare an email summary based on generated research.

Current implementation:

✅ Creates email content  
✅ Requires user approval  
✅ Demonstrates safe external action handling  
✅ Uses dry-run mode  

Future improvement:

- Real Gmail API integration
- Real email delivery


## 🔐 Human Approval System

The agent does not automatically perform risky actions.

Example:

APPROVAL NEEDED

Tool:
send_email

Approve this action? (y/n)


The user decides whether the action should continue.


## 📜 Audit Logging

Every agent action is recorded.

Logs include:

1. User request
2. Tool calls
3. Tool results
4. Approval decisions
5. Completion status
6. Timestamp

Example:

logs/
└── run-2026-08-03.log



## 🛡️ Iteration Protection

The agent has a maximum iteration limit.

This prevents:

1. Infinite loops
2. Uncontrolled execution
3. Unexpected resource usage

Configured in:


config.py


# 🏗️ Project Structure


personal-task-agent/

│
├── agent.py
│   └── Main AI reasoning and execution loop
│
├── tools.py
│   └── Research, save_note, send_email tools
│
├── config.py
│   └── Model settings and permissions
│
├── requirements.txt
│
├── .env
│   └── API configuration
│
├── README.md
│
├── notes/
│   └── Generated research files
│
└── logs/
    └── Agent execution history



# 🧠 Agent Architecture


                 User
                  |
                  |
                  ▼
            Agent Controller
              agent.py
                  |
        ---------------------
        |         |          |
        ▼         ▼          ▼
   Research   Save Note   Email
    Tool       Tool       Tool
        |         |          |
        ▼         ▼          ▼
   Information  File     Approval
                         Required
                              |
                              ▼
                           Logging


# 🛠️ Tools

## 1. Research Tool

Purpose:

Generate useful research information about a requested topic.

Example:

Research artificial intelligence


Output:

Structured research notes



## 2. Save Note Tool

Purpose:

Save generated information into the notes directory.

Example:


notes/topic.md



## 3. Send Email Tool

Purpose:

Create an email summary.

Safety:

1. Requires approval
2. Controlled by the human user
3. Currently implemented as a dry-run

Example output:


(dry-run) email prepared but not actually sent



# ⚙️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Main programming language |
| OpenAI Compatible API | AI model communication |
| python-dotenv | Environment variable management |
| JSON Tool Calling | Agent tool execution |
| Markdown | Note storage format |
| File System | Memory and logging |


# 🚀 Installation

## 1. Clone Repository

git clone <repository-url>

## 2. Open Project Folder


cd personal-task-agent


## 3. Install Dependencies


pip install -r requirements.txt


# 🔑 Environment Setup

Create a `.env` file:

OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://openrouter.ai/api/v1


Never upload your `.env` file publicly.


# ▶️ Running the Agent

Run:

python agent.py "Research black holes, save notes to blackholes.md, then email a summary to Jahanzebsiyal4@outlook.com"




# 📂 Output Example

After execution:

## Generated Notes


notes/
└── blackholes.md


## Execution Logs

logs/
└── run-xxxx.log


---

# 🖥️ Example Execution


GOAL
Research black holes

↓

CALL research

↓

RESULT
Research completed

↓

CALL save_note

↓

RESULT
Saved notes/blackholes.md

↓

APPROVAL NEEDED
send_email

↓

USER APPROVED

↓

DONE


# 🔒 Safety Design

## Human-in-the-loop Approval

Actions with external impact require permission.

Example:


send_email
        |
        ▼
Human Approval
        |
        ▼
Execution



## Logging System

The system records every important event:

Timestamp
↓
Action
↓
Result
↓
Approval


## Execution Limit

The agent cannot continue forever.

Maximum turns are controlled by:

MAX_ITERATIONS


# 📚 Learning Outcomes

This project demonstrates:

✅ AI Agent Development  
✅ Autonomous Task Execution  
✅ Tool Calling  
✅ Multi-step Reasoning  
✅ Human Approval Workflows  
✅ Secure API Handling  
✅ Logging Systems  
✅ Safe AI Design  


# 🔮 Future Improvements

Future versions can include:

1. 🌐 Real web search integration
2. 📧 Gmail API email sending
3. 📄 PDF research extraction
4. 🖥️ Streamlit web interface
5. ✅ Task management system
6. 🧠 Long-term memory
7. 🔗 External API integrations


# 👥 Contributors

| Name | Role |
|------|------|
| Jahanzaib Muhammad Talib | Developer |

---

# 💻 Languages

| Language | Percentage |
|----------|------------|
| Python | 100% |

---

# 📊 Repository Information

**Project Name:** Personal Task Agent  
<br>
**Project Type:** AI Agent Application  
<br>
**Primary Language:** Python  
<br>
**Architecture:** Tool-Based Autonomous Agent  
<br>
**Status:** Completed ✅

---

# 👨‍💻 Author

Jahanzaib Muhammad Talib

📧 Jahanzebsiyal4@outlook.com

Module 3 – Week 4 Project

Personal Task Agent

