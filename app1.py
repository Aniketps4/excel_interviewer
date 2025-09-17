import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Predefined questions and rubrics
QUESTIONS = [
    {
        "question": "Explain the difference between relative and absolute cell references in Excel.",
        "ideal": "Relative references change when copied (e.g., A1 becomes B1). Absolute uses $ (e.g., $A$1 stays fixed). Mixed like $A1 fixes column."
    },
    {
        "question": "How would you use VLOOKUP to find a value in a table? Provide an example formula.",
        "ideal": "VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup]). Example: =VLOOKUP(A2, B2:D100, 3, FALSE) for exact match."
    },
    {
        "question": "What is a pivot table and how do you create one in Excel?",
        "ideal": "Summarizes data. Select data > Insert > PivotTable > Choose location > Drag fields to rows/columns/values."
    },
    {
        "question": "Describe how to use conditional formatting in Excel.",
        "ideal": "Highlights cells based on rules. Home > Conditional Formatting > Choose rule (e.g., greater than) > Set format."
    },
    {
        "question": "How can you remove duplicates from a dataset in Excel?",
        "ideal": "Select data > Data > Remove Duplicates > Choose columns."
    }
]

def convert_to_gemini_contents(messages):
    """Convert OpenAI-like messages to Gemini contents format."""
    contents = []
    for msg in messages:
        role = msg["role"]
        if role == "system":
            if not contents:
                contents.append({"role": "user", "parts": [{"text": msg["content"]}]})
            else:
                contents[-1]["parts"][0]["text"] += f"\n\nSystem instruction: {msg["content"]}"
        elif role == "user":
            contents.append({"role": "user", "parts": [{"text": msg["content"]}]})
        elif role == "assistant":
            contents.append({"role": "model", "parts": [{"text": msg["content"]}]})
    return contents

def get_llm_response(messages, model="gemini-2.5-flash"):
    """Get response using Gemini."""
    model = genai.GenerativeModel(model)
    contents = convert_to_gemini_contents(messages)
    response = model.generate_content(contents)
    return response.text if response.text else "Error: No response generated."

# Streamlit app
st.title("Excel Skills Assessor (Gemini Edition)")

if "stage" not in st.session_state:
    st.session_state.stage = "intro"
    st.session_state.current_question = 0
    st.session_state.responses = []
    st.session_state.scores = []
    st.session_state.history = []

# Display chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Your response...")

if st.session_state.stage == "intro":
    intro = "Hello! I'm your AI Excel Interviewer powered by Google Gemini. We'll go through 5 questions to assess your skills. Answer clearly, and I'll evaluate. Ready? Type 'start'."
    st.session_state.history.append({"role": "assistant", "content": intro})
    st.session_state.stage = "waiting_start"
    st.rerun()

elif st.session_state.stage == "waiting_start":
    if user_input and user_input.lower() == "start":
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.stage = "question"
        st.rerun()

elif st.session_state.stage == "question":
    if st.session_state.current_question < len(QUESTIONS):
        q = QUESTIONS[st.session_state.current_question]["question"]
        st.session_state.history.append({"role": "assistant", "content": q})
        st.session_state.stage = "answer"
        st.rerun()
    else:
        st.session_state.stage = "summary"
        st.rerun()

elif st.session_state.stage == "answer":
    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.responses.append(user_input)
        
        # Evaluate response
        ideal = QUESTIONS[st.session_state.current_question]["ideal"]
        eval_prompt = [
            {"role": "system", "content": "You are an expert Excel evaluator. Score the user's answer (0-5) for correctness, completeness, clarity. Provide total score and brief reasoning."},
            {"role": "user", "content": f"Ideal: {ideal}\nUser: {user_input}"}
        ]
        eval_response = get_llm_response(eval_prompt)
        score = eval_response
        st.session_state.scores.append(score)
        
        # Decide if follow-up needed
        follow_prompt = [
            {"role": "system", "content": "If the answer is incomplete or unclear, suggest a short follow-up question. Else, say 'None'."},
            {"role": "user", "content": user_input}
        ]
        follow_up = get_llm_response(follow_prompt)
        if follow_up.strip() != "None":
            st.session_state.history.append({"role": "assistant", "content": follow_up})
            st.rerun()
        else:
            st.session_state.current_question += 1
            st.session_state.stage = "question"
            st.rerun()

elif st.session_state.stage == "summary":
    # Generate report
    report_prompt = [
        {"role": "system", "content": "Summarize performance: Overall score, strengths, weaknesses, tips. Based on responses and scores."},
        {"role": "user", "content": f"Responses: {st.session_state.responses}\nScores: {st.session_state.scores}"}
    ]
    report = get_llm_response(report_prompt)
    st.session_state.history.append({"role": "assistant", "content": report})
    st.rerun()