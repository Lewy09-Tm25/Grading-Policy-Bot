import streamlit as st
import logging
from core.prompts import get_system_prompt
from client.llm_client import stream_openai_response

# ==========================================
# 1. Logging Configuration
# ==========================================
# This sets up the terminal output so you can track the app's exact state.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

logger.info("=== Application Starting/Re-running ===")

# ==========================================
# 2. Page Configuration & Caching
# ==========================================
st.set_page_config(
    page_title="CUNY Grade Glossary Advisor",
    # page_icon="🎓",
    layout="centered"
)

# @st.cache_data ensures the massive Markdown file is only read from the disk ONCE
# when the app first spins up, rather than on every single button click.
@st.cache_data(show_spinner=False)
def load_cached_prompt():
    logger.info("Cache Miss: Loading Markdown document from disk and building System Prompt.")
    return get_system_prompt()

# ==========================================
# 3. State Management Initialization
# ==========================================
# Streamlit clears variables on every interaction unless stored in session_state.
if "messages" not in st.session_state:
    logger.info("Initializing new user session state.")
    st.session_state.messages = []
    
    # Load the system prompt and append it as the invisible first message
    system_prompt = load_cached_prompt()
    st.session_state.messages.append({
        "role": "system",
        "content": system_prompt
    })
    logger.info("System Prompt successfully injected into conversation memory.")

# ==========================================
# 4. User Interface Rendering
# ==========================================
st.title("🎓 CUNY Academic Policy Bot")
st.markdown("Ask me any questions regarding the **Uniform Grade Glossary, Policies, and Guidelines**.")

logger.info(f"Rendering {len(st.session_state.messages)} messages to the UI.")

# Loop through memory and draw the chat bubbles on the screen
for msg in st.session_state.messages:
    # CRITICAL: We skip the 'system' role so the user doesn't see the 11-page document
    if msg["role"] == "system":
        continue
    
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 5. Core Interaction Loop
# ==========================================
# This halts execution until the user types something and hits enter.
if user_input := st.chat_input("E.g., What is the WU grade for?"):
    
    logger.info(f"User Input Received: '{user_input}'")
    
    # 1. Save user input to memory
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Display the user's message instantly
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # 3. Call the Engine and Stream the Response
    with st.chat_message("assistant"):
        logger.info("Initiating streaming connection to OpenAI...")
        
        # We pass the entire message array (including the hidden system prompt)
        stream = stream_openai_response(st.session_state.messages)
        
        # st.write_stream automatically iterates over the generator and simulates typing
        full_response = st.write_stream(stream)
        
        logger.info("Stream complete. Rendering final response.")
        
    # 4. Save the finalized assistant response to memory so it remembers context
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    logger.info("Assistant response saved to session state.")