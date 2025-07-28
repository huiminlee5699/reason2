import streamlit as st
import time
import random
from openai import OpenAI

def generate_reasoning_steps_for_credibility_task():
    """Generate realistic reasoning steps for the social media credibility evaluation task."""
    
    reasoning_steps = [
        "I need to evaluate this social media post about green tea and cancer prevention for credibility. Let me break down the claims systematically.",
        "First, I'll examine the specific claims: 1) A peer-reviewed Stanford study exists, 2) 50,000 participants over 10 years, 3) 87% cancer risk reduction from 3 cups daily, 4) 'Big Pharma doesn't want you to know.'",
        "Checking the methodology claims: A 10-year study with 50,000 participants sounds plausible for epidemiological research, but I need to verify if such a study actually exists from Stanford.",
        "The 87% risk reduction is an extremely high effect size that would be groundbreaking if true. Such dramatic results would typically be widely reported in major medical journals and news outlets.",
        "Red flags I'm noticing: 1) The 'Big Pharma conspiracy' language, 2) Urgency to 'share before they take it down,' 3) Hashtags like #GreenTeaCure suggest oversimplification, 4) No citation of the actual study.",
        "I should also consider what legitimate research says about green tea and cancer. While some studies suggest modest benefits, the scientific consensus doesn't support such dramatic claims.",
        "The post uses persuasive but unscientific language patterns common in health misinformation: definitive claims ('proves'), conspiracy theories, and emotional appeals.",
        "Based on my analysis, this appears to be misleading health information that could potentially harm people by promoting false hope or delaying proper medical care."
    ]
    
    return reasoning_steps

# Custom CSS for clean, minimal ChatGPT-like interface
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
        margin: 12px 16px; padding: 12px; background-color: #ffffff;
        border-left: 3px solid #e1e5e9; border-radius: 6px; animation: fadeIn 0.3s ease-in;
        line-height: 1.5; font-size: 16px; color: #2d2d2d;
    }
    .done-indicator {
        display: flex; align-items: center; gap: 6px; color: #10b981;
        font-size: 14px; margin-top: 12px; font-weight: 500;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
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
if "show_reasoning" not in st.session_state:
    st.session_state.show_reasoning = {}
if "live_reasoning" not in st.session_state:
    st.session_state.live_reasoning = {}
if "reasoning_step_counter" not in st.session_state:
    st.session_state.reasoning_step_counter = 0

# Display chat history
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        if "reasoning" in message:
            thinking_duration = message.get("thinking_duration", 0)
            with st.expander(f"💭 Thought for {thinking_duration} seconds", expanded=False):
                for j, step in enumerate(message["reasoning"], start=1):
                    st.markdown(f'<div class="reasoning-step"><strong>Step {j}:</strong> {step}</div>', unsafe_allow_html=True)
                st.markdown('<div class="done-indicator">✓ Done</div>', unsafe_allow_html=True)

# Chat input & live reasoning
if prompt := st.chat_input("Ask anything..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="user-message">{prompt}</div>', unsafe_allow_html=True)

    # Reset reasoning
    st.session_state.current_reasoning_history = []
    st.session_state.reasoning_step_counter += 1

    # Generate steps & start timing
    reasoning_steps = generate_reasoning_steps_for_credibility_task()
    start_time = time.time()

    # Live reasoning expander with "Show thinking ▼"
    exp = st.expander("Show thinking ▼", expanded=False)
    placeholder = exp.empty()

    for step in reasoning_steps:
        st.session_state.current_reasoning_history.append(step)
        # Build HTML for each step (only left border)
        html = "".join(
            f'<div class="reasoning-step"><strong>Step {i+1}:</strong> {s}</div>'
            for i, s in enumerate(st.session_state.current_reasoning_history)
        )
        placeholder.markdown(html, unsafe_allow_html=True)
        time.sleep(2.5)

    thinking_duration = int(time.time() - start_time)
    placeholder.empty()

    # Call OpenAI
    try:
        full_response = ""
        stream = client.chat.completions.create(
            model="o1-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        response_ph = st.empty()
        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_ph.markdown(f'<div class="assistant-message">{full_response}</div>', unsafe_allow_html=True)

        # Store assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "reasoning": st.session_state.current_reasoning_history.copy(),
            "thinking_duration": thinking_duration
        })

        # Rerun to show the new message + expander
        st.rerun()

    except Exception as e:
        st.error(f"Error generating response: {e}")

# JavaScript for auto-resize
st.components.v1.html("""
<script>
function setupAutoResize() {
    const textareas = document.querySelectorAll('.stChatInput textarea');
    textareas.forEach(textarea => {
        if (!textarea.hasAttribute('data-auto-resize-setup')) {
            textarea.setAttribute('data-auto-resize-setup', 'true');
            textarea.style.height = '48px';
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 200) + 'px';
            });
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    setTimeout(() => { this.style.height = '48px'; }, 100);
                }
            });
            textarea.addEventListener('blur', function() {
                if (this.value.trim() === '') { this.style.height = '48px'; }
            });
        }
    });
}
setInterval(setupAutoResize, 500);
setupAutoResize();
</script>
""", height=0)
