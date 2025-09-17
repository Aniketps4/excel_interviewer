Excel Skills Assessor

A conversational AI-powered interviewer to assess Microsoft Excel skills, built with Python, Streamlit, and Google Gemini API. The agent conducts a structured, multi-turn interview, evaluates responses, and provides a performance summary with feedback. Designed as a proof-of-concept (PoC) for hiring managers and candidates to evaluate or practice Excel proficiency.

Features
Structured Interview Flow: Introduces itself, asks 5 Excel-related questions (beginner to advanced), and provides a concluding report.
Intelligent Evaluation: Uses Google Gemini 2.5 Flash to score responses on correctness, completeness, and clarity.
Agentic Behavior: Simulates a human interviewer with adaptive follow-up questions for incomplete or unclear answers.
Feedback Report: Summarizes performance with scores, strengths, weaknesses, and improvement tips.
Web Interface: Deployed as a Streamlit app for easy access and interaction.

Prerequisites
Python: 3.9 or higher (3.12 recommended).
Git: For cloning and managing the repository.
Google Gemini API Key: Obtain from Google AI Studio.
GitHub Account: For deployment to Streamlit Community Cloud.
Streamlit Community Cloud Account: Sign up at share.streamlit.io with GitHub.


Usage
Open the deployed URL app (https://excelinterviewer-o6dpiudvbaigf4ik5mdkmt.streamlit.app/).
Type start to begin.
Answer 5 Excel questions (e.g., VLOOKUP, PivotTables).
Receive real-time evaluations and a final performance report.
Example questions:
"Explain the difference between relative and absolute cell references."
"How would you use INDEX and MATCH together?"

Sample Transcript

AI: Hello! I'm your AI Excel Interviewer powered by Google Gemini. Type 'start'.
User: start
AI: Question 1: What is the purpose of the AutoSum feature in Excel, and how do you use it?
User: It sums numbers. Click Σ and Enter.
AI: Can you mention other functions AutoSum supports?
User: Like average or count.

Future Enhancements
Integrate Google Sheets API for task-based assessments (e.g., validate formulas in a sheet).
Add user authentication for private access.
Expand question bank with VBA, Power Query, or advanced formulas.
Log anonymized sessions to build a dataset for fine-tuning.

Troubleshooting

Local Errors:
ModuleNotFoundError: Run pip install -r requirements.txt.
NameError: name 'st' is not defined: Ensure import streamlit as st in app1.py.
401 Unauthorized: Verify GEMINI_API_KEY in .env or regenerate at Google AI Studio.

Deployment Errors:
Check Streamlit Cloud logs (dashboard).
Ensure requirements.txt is correct and GEMINI_API_KEY is in Secrets.

Git Issues:
If git push fails, try git pull origin main --rebase or git push -f (careful).



See Streamlit Docs or Gemini API Docs.
