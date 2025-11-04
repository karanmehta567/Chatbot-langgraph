import streamlit as st
from langgraph_backend import workflow,retrive_all
from langchain_core.messages import HumanMessage
import uuid

# Helper function to create id
def create_unique_id():
    return str(uuid.uuid4())

# Reset chat (when user clicks on new chat, this function will trigger)
def reset_chat():
    new_thread_id = create_unique_id()
    st.session_state['current_thread'] = new_thread_id
    st.session_state['message_history'] = []
    add_thread(new_thread_id)
    st.rerun()

# Add that newly generated thread to list
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# Load conversation for a thread
def load_conversation(thread_id):
    try:
        data = workflow.get_state(config={'configurable': {'thread_id': thread_id}})
        messages = data.values.get('messages', [])
        formatted = []
        for msg in messages:
            if msg.type == "human":
                formatted.append({'role': 'user', 'content': msg.content})
            elif msg.type == "ai":
                formatted.append({'role': 'assistant', 'content': msg.content})
        return formatted
    except Exception as e:
        st.warning(f"Could not load thread {thread_id}: {e}")
        return []

# ---------------- SESSION SETUP ----------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_all()

if 'current_thread' not in st.session_state:
    st.session_state['current_thread'] = create_unique_id()
    add_thread(st.session_state['current_thread'])

# ---------------- SIDEBAR ----------------
st.sidebar.title('Chatbot using Langgraph')

if st.sidebar.button('🆕 New Chat'):
    reset_chat()

st.sidebar.markdown("### Active Thread ID")
st.sidebar.code(st.session_state['current_thread'])

# List all previous threads
if st.session_state['chat_threads']:
    st.sidebar.markdown("### Previous Threads")
    for t in st.session_state['chat_threads']:
        # Make each thread clickable
        if st.sidebar.button(t):
            st.session_state['current_thread'] = t
            st.session_state['message_history'] = load_conversation(t)
            st.rerun()

# ---------------- CHAT DISPLAY ----------------
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# ---------------- USER INPUT ----------------
user_input = st.chat_input('Type Here')

if user_input:
    config = {'configurable': {'thread_id': st.session_state['current_thread']}}
    
    # Show user message
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # Stream assistant response
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in workflow.stream(
                {'messages': [HumanMessage(content=user_input)]},
                stream_mode='messages',
                config=config
            )
        )

    # Save assistant reply
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
