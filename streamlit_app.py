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
    
    /* Interactive reasoning dropdown styling */
    .reasoning-toggle-container {
        background-color: #f8f9fa;
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        margin: 16px 0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .reasoning-toggle-header {
        padding: 12px 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #f8f9fa;
        border-radius: 8px;
        transition: background-color 0.2s;
        font-size: 14px;
        color: #6b7280;
        font-weight: 500;
        border: none;
        width: 100%;
        text-align: left;
    }
    
    .reasoning-toggle-header:hover {
        background-color: #f1f3f4;
        color: #4b5563;
    }
    
    .reasoning-content {
        max-height: 400px;
        overflow-y: auto;
        border-top: 1px solid #e1e5e9;
        background-color: #f8f9fa;
        border-radius: 0 0 8px 8px;
    }
    
    .reasoning-step {
        margin: 12px 16px;
        padding: 12px;
        background-color: #ffffff;
        border-radius: 6px;
        border-left: 3px solid #e1e5e9;
        line-height: 1.5;
        font-size: 16px;
        color: #2d2d2d;
        animation: fadeIn 0.3s ease-in;
    }
    
    .thinking-indicator {
        padding: 16px;
        text-align: center;
        color: #6b7280;
        font-style: italic;
        background-color: #f8f9fa;
    }
    
    .chevron {
        transition: transform 0.2s;
        font-size: 12px;
    }
    
    .chevron.expanded {
        transform: rotate(180deg);
    }
    
    /* Style for Streamlit buttons to make them invisible */
    .reasoning-button {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        width: 100% !important;
    }
    
    .reasoning-button > div {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
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
if "reasoning_step_counter" not in st.session_state:
    st.session_state.reasoning_step_counter = 0
if "show_reasoning" not in st.session_state:
    st.session_state.show_reasoning = {}  # Track which messages have reasoning expanded
if "live_reasoning" not in st.session_state:
    st.session_state.live_reasoning = {}  # Track live reasoning for current generation

# Display existing messages with custom styling
for i, message in enumerate(st.session_state.messages):
    message_key = f"msg_{i}"
    
    if message["role"] == "user":
        # User message - right aligned, light grey
        st.markdown(f"""
        <div class="user-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        # Assistant message - left aligned
        st.markdown(f"""
        <div class="assistant-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
        
        # If it's an assistant message with reasoning, show the interactive dropdown
        if "reasoning" in message:
            thinking_duration = message.get("thinking_duration", 0)
            
            # Create the reasoning toggle container
            st.markdown(f"""
            <div class="reasoning-toggle-container">
            """, unsafe_allow_html=True)
            
            # Create columns for the toggle button
            col1, col2 = st.columns([1, 0.1])
            
            with col1:
                # Toggle button for reasoning
                is_expanded = st.session_state.show_reasoning.get(message_key, False)
                chevron = "▼" if is_expanded else "▶"
                
                if st.button(f"{chevron} Thought for {thinking_duration} seconds", 
                           key=f"reasoning_toggle_{message_key}",
                           help="Click to show/hide reasoning"):
                    st.session_state.show_reasoning[message_key] = not is_expanded
                    st.rerun()
            
            # Show reasoning content if expanded
            if st.session_state.show_reasoning.get(message_key, False):
                st.markdown('<div class="reasoning-content">', unsafe_allow_html=True)
                
                for j, step in enumerate(message["reasoning"], 1):
                    st.markdown(f"""
                    <div class="reasoning-step">
                        <strong>Step {j}:</strong> {step}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add "Done" indicator at the end
                st.markdown("""
                <div class="done-indicator" style="margin: 12px 16px 16px 16px;">
                    ✓ Done
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add action buttons (copy, upvote, downvote)
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
    st.session_state.messages.append({"role": "user", "content": prompt))
    
    # Display the user message immediately
    st.markdown(f"""
    <div class="user-message">
        {prompt}
    </div>
    """, unsafe_allow_html=True)
    
    # Reset reasoning history for new conversation
    st.session_state.current_reasoning_history = []
    st.session_state.reasoning_step_counter += 1
    current_msg_key = f"msg_live_{st.session_state.reasoning_step_counter}"
    
    # Generate reasoning steps for the credibility task
    reasoning_steps = generate_reasoning_steps_for_credibility_task()
    
    # Track timing for the "Thought for X seconds" feature
    start_time = time.time()
    
    # Create the interactive reasoning container during generation
    st.markdown(f"""
    <div class="reasoning-toggle-container">
    """, unsafe_allow_html=True)
    
    # Create toggle for live reasoning - default to collapsed
    col1, col2 = st.columns([1, 0.1])
    
    with col1:
        live_expanded = st.session_state.show_reasoning.get(current_msg_key, False)
        chevron = "▼" if live_expanded else "▶"
        
        if st.button(f"{chevron} Thinking...", 
                   key=f"live_reasoning_toggle_{current_msg_key}",
                   help="Click to show/hide reasoning as it develops"):
            st.session_state.show_reasoning[current_msg_key] = not live_expanded
            st.rerun()
    
    # Live reasoning content area
    reasoning_content_container = st.empty()
    
    # Always build the reasoning history but only show if dropdown is open
    for i, step in enumerate(reasoning_steps):
        st.session_state.current_reasoning_history.append(step)
        
        # Only display if user has opened the dropdown
        if st.session_state.show_reasoning.get(current_msg_key, False):
            # Update the reasoning content with all steps accumulated so far
            content_html = '<div class="reasoning-content">'
            for j, hist_step in enumerate(st.session_state.current_reasoning_history, 1):
                content_html += f"""
                <div class="reasoning-step">
                    <strong>Step {j}:</strong> {hist_step}
                </div>
                """
            content_html += '</div>'
            
            reasoning_content_container.markdown(content_html, unsafe_allow_html=True)
        
        time.sleep(2.5)  # Time to read the reasoning step
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate total thinking time
    end_time = time.time()
    thinking_duration = int(end_time - start_time)
    
    # Clear the live reasoning container
    reasoning_content_container.empty()
    
    # Get actual response from OpenAI
    try:
        stream = client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        # Capture the response
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
        message_data = {
            "role": "assistant", 
            "content": full_response, 
            "reasoning": st.session_state.current_reasoning_history,
            "thinking_duration": thinking_duration
        }
        st.session_state.messages.append(message_data)
        
        # Clean up live reasoning state
        if current_msg_key in st.session_state.show_reasoning:
            del st.session_state.show_reasoning[current_msg_key]
        
        st.rerun()
        
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
