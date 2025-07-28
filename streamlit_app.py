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

# Custom CSS for clean, minimal ChatGPT-like interface with interactive reasoning
st.markdown("""
<style>
    .stApp {
        background-color: white;
    }
    
    .main-title {
        text-align: center;
        font-size: 28px;
        font-weight: 400;
        color: #2d2d2d;
        margin-bottom: 30px;
        margin-top: 20px;
    }
    
    .chat-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .user-message {
        background-color: #f0f0f0;
        border: 1px solid #d1d5db;
        border-radius: 18px;
        padding: 12px 16px;
        margin: 8px 0 8px auto;
        max-width: 70%;
        text-align: left;
        font-size: 16px;
        color: #2d2d2d;
        line-height: 1.5;
    }
    
    .assistant-message {
        background-color: white;
        padding: 12px 0;
        margin: 8px 0;
        max-width: 100%;
        text-align: left;
        font-size: 16px;
        color: #2d2d2d;
        line-height: 1.6;
    }
    
    .action-buttons {
        display: flex;
        gap: 8px;
        margin-top: 12px;
        padding-top: 8px;
        justify-content: flex-start;
    }
    
    .action-button {
        background: none;
        border: none;
        cursor: pointer;
        padding: 6px;
        border-radius: 4px;
        color: #9ca3af;
        font-size: 16px;
        transition: background-color 0.2s;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .action-button:hover {
        background-color: #f3f4f6;
        color: #6b7280;
    }
    
    .done-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        color: #10b981;
        font-size: 14px;
        margin-top: 12px;
        font-weight: 500;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Hide default Streamlit chat styling */
    .stChatMessage {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .stChatMessage > div {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Auto-expanding chat input */
    .stChatInput {
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .stChatInput textarea {
        min-height: 48px !important;
        max-height: 200px !important;
        resize: none !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
        overflow-y: auto !important;
        transition: height 0.2s ease !important;
    }
    
    /* Make container wider */
    .main .block-container {
        max-width: 1000px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Show title
st.markdown('<h1 class="main-title">What\'s on the agenda today?</h1>', unsafe_allow_html=True)

# Use the API key from Streamlit secrets
openai_api_key = st.secrets["openai_api_key"]

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_reasoning_history" not in st.session_state:
    st.session_state.current_reasoning_history = []
# (retain the old toggles state even though we no longer use it)
if "show_reasoning" not in st.session_state:
    st.session_state.show_reasoning = {}
if "live_reasoning" not in st.session_state:
    st.session_state.live_reasoning = {}
if "reasoning_step_counter" not in st.session_state:
    st.session_state.reasoning_step_counter = 0

# Display existing messages with custom styling
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

        # --- REPLACED: Manual CSS dropdown with st.expander ---
        if "reasoning" in message:
            thinking_duration = message.get("thinking_duration", 0)
            with st.expander(f"💭 Thought for {thinking_duration} seconds", expanded=False):
                for j, step in enumerate(message["reasoning"], start=1):
                    st.markdown(f"""
                    <div class="reasoning-step">
                        <strong>Step {j}:</strong> {step}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("""
                <div class="done-indicator">
                    ✓ Done
                </div>
                """, unsafe_allow_html=True)
            # (you can leave your action-buttons here if you still want them)
            st.markdown("""
            <div class="action-buttons">
                <button class="action-button" onclick="navigator.clipboard.writeText(document.querySelector('.assistant-message').innerText)" title="Copy">
                    📋
                </button>
                <button class="action-button" title="Upvote">
                    👍
                </button>
                <button class="action-button" title="Downvote">
                    👎
                </button>
            </div>
            """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask anything..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the user message immediately
    st.markdown(f"""
    <div class="user-message">
        {prompt}
    </div>
    """, unsafe_allow_html=True)
    
    # Reset reasoning history for new conversation
    st.session_state.current_reasoning_history = []
    st.session_state.reasoning_step_counter += 1
    # (we keep current_msg_key around, though expander no longer needs it)
    current_msg_key = f"msg_live_{st.session_state.reasoning_step_counter}"
    
    # Generate reasoning steps for the credibility task
    reasoning_steps = generate_reasoning_steps_for_credibility_task()
    
    # Track timing for the "Thinking..." feature
    start_time = time.time()
    
    # --- REPLACED: Manual live dropdown with st.expander + placeholder ---
    exp = st.expander("💭 Thinking...", expanded=False)
    placeholder = exp.empty()
    
    for i, step in enumerate(reasoning_steps, start=1):
        st.session_state.current_reasoning_history.append(step)
        # build cumulative markdown
        md = "\n\n".join(
            f"**Step {j}:** {s}"
            for j, s in enumerate(st.session_state.current_reasoning_history, start=1)
        )
        placeholder.markdown(md)
        time.sleep(2.5)
    
    thinking_duration = int(time.time() - start_time)
    placeholder.empty()
    
    # Get actual response from OpenAI
    try:
        stream = client.chat.completions.create(
            model="o1-mini",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )
        
        response_placeholder = st.empty()
        full_response = ""
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                response_placeholder.markdown(f"""
                <div class="assistant-message">
                    {full_response}
                </div>
                """, unsafe_allow_html=True)
        
        # Store message with reasoning and timing
        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response, 
            "reasoning": st.session_state.current_reasoning_history.copy(),
            "thinking_duration": thinking_duration
        })
        
        st.experimental_rerun()
        
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")

# Add JavaScript for auto-resizing functionality
st.components.v1.html("""
<script>
function setupAutoResize() {
    const textareas = document.querySelectorAll('.stChatInput textarea');
    textareas.forEach(textarea => {
        if (!textarea.hasAttribute('data-auto-resize-setup')) {
            textarea.setAttribute('data-auto-resize-setup', 'true');
            
            // Set initial height
            textarea.style.height = '48px';
            
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 200) + 'px';
            });
            
            textarea.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    setTimeout(() => {
                        this.style.height = '48px';
                    }, 100);
                }
            });
            
            // Reset height when textarea is empty
            textarea.addEventListener('blur', function() {
                if (this.value.trim() === '') {
                    this.style.height = '48px';
                }
            });
        }
    });
}

// Run setup periodically to catch new elements
setInterval(setupAutoResize, 500);
setupAutoResize();
</script>
""", height=0)

