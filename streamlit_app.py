import streamlit as st
import time
import random
from openai import OpenAI

def generate_reasoning_steps_for_credibility_task():
    """Generate realistic reasoning steps for the social media credibility evaluation task."""
    return [
        "I need to evaluate this social media post about green tea and cancer prevention for credibility. Let me break down the claims systematically.",
        "First, I'll examine the specific claims: 1) A peer-reviewed Stanford study exists, 2) 50,000 participants over 10 years, 3) 87% cancer risk reduction from 3 cups daily, 4) 'Big Pharma doesn't want you to know.'",
        "Checking the methodology claims: A 10-year study with 50,000 participants sounds plausible for epidemiological research, but I need to verify if such a study actually exists from Stanford.",
        "The 87% risk reduction is an extremely high effect size that would be groundbreaking if true. Such dramatic results would typically be widely reported in major medical journals and news outlets.",
        "Red flags I'm noticing: 1) The 'Big Pharma conspiracy' language, 2) Urgency to 'share before they take it down,' 3) Hashtags like #GreenTeaCure suggest oversimplification, 4) No citation of the actual study.",
        "I should also consider what legitimate research says about green tea and cancer. While some studies suggest modest benefits, the scientific consensus doesn't support such dramatic claims.",
        "The post uses persuasive but unscientific language patterns common in health misinformation: definitive claims ('proves'), conspiracy theories, and emotional appeals.",
        "Based on my analysis, this appears to be misleading health information that could potentially harm people by promoting false hope or delaying proper medical care."
    ]

# Custom CSS: hide default expander arrow & remove its border
st.markdown("""
<style>
    .stApp { background-color: white; }
    .main-title { text-align: center; font-size: 28px; font-weight: 400; color: #2d2d2d; margin: 20px 0; }
    .user-message {
        background-color: #f0f0f0; border: 1px solid #d1d5db; border-radius: 18px;
        padding: 12px 16px; margin: 8px 0 8px auto; max-width: 70%; font-size: 16px; color: #2d2d2d; line-height: 1.5;
    }
    .assistant-message {
        background-color: white; padding: 12px 0; margin: 8px 0; max-width: 100%;
        font-size: 16px; color: #2d2d2d; line-height: 1.6;
    }
    .reasoning-step {
        margin: 12px 16px; padding: 12px 0 12px 16px;  /* only left padding */
        background-color: transparent;
        border-left: 3px solid #e1e5e9;  /* subtle left line */
        line-height: 1.5; font-size: 16px; color: #2d2d2d;
    }
    .done-indicator {
        display: flex; align-items: center; gap: 6px; color: #10b981;
        font-size: 14px; margin: 12px 16px; font-weight: 500;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    /* hide the default expander arrow */
    [data-testid="stExpanderHeader"] svg { display: none !important; }
    /* remove expander border/shadow */
    [data-testid="stExpander"] > div:first-child,
    [data-testid="stExpanderContent"] { border: none !important; box-shadow: none !important; padding: 0 !important; margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">What\'s on the agenda today?</h1>', unsafe_allow_html=True)

# OpenAI client
openai_api_key = st.secrets["openai_api_key"]
client = OpenAI(api_key=openai_api_key)

# Session state init
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_reasoning_history" not in st.session_state:
    st.session_state.current_reasoning_history = []
if "reasoning_step_counter" not in st.session_state:
    st.session_state.reasoning_step_counter = 0

# Render chat history: show "Show thinking" expander BEFORE each assistant message
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        if "reasoning" in msg:
            with st.expander("Show thinking ▼", expanded=False):
                for i, step in enumerate(msg["reasoning"], start=1):
                    st.markdown(f'<div class="reasoning-step"><strong>Step {i}:</strong> {step}</div>', unsafe_allow_html=True)
                st.markdown('<div class="done-indicator">✓ Done</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

# Chat input & live reasoning
if prompt := st.chat_input("Ask anything..."):
    # append & display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)

    # reset reasoning history
    st.session_state.current_reasoning_history = []
    st.session_state.reasoning_step_counter += 1

    # generate reasoning steps & time it
    reasoning_steps = generate_reasoning_steps_for_credibility_task()
    start_time = time.time()

    # live reasoning expander
    exp = st.expander("Show thinking ▼", expanded=False)
    placeholder = exp.empty()
    for step in reasoning_steps:
        st.session_state.current_reasoning_history.append(step)
        html = "".join(
            f'<div class="reasoning-step"><strong>Step {i+1}:</strong> {s}</div>'
            for i, s in enumerate(st.session_state.current_reasoning_history)
        )
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(2.5)
    placeholder.empty()
    thinking_duration = int(time.time() - start_time)

    # call OpenAI & stream answer
    full_response = ""
    response_ph = st.empty()
    try:
        stream = client.chat.completions.create(
            model="o1-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_ph.markdown(f'<div class="assistant-message">{full_response}</div>', unsafe_allow_html=True)

        # store assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "reasoning": st.session_state.current_reasoning_history.copy()
        })

        # rerun so the expander now appears above the new response
        st.rerun()

    except Exception as e:
        st.error(f"Error generating response: {e}")
