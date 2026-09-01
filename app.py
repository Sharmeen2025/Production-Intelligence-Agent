import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from graph import agent_executor

st.set_page_config(
    page_title="Production Intelligence Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimalist Custom CSS
st.markdown("""
<style>
    .header-container { display: flex; align-items: center; gap: 12px; margin-bottom: 2rem; }
    .title-text { font-size: 1.5rem; font-weight: 600; color: #0F172A; margin: 0; }
</style>
""", unsafe_allow_html=True)

# Consumer-style Sidebar
with st.sidebar:
    st.markdown("### Settings")
    st.toggle("Enable Web Search", value=True)
    st.toggle("Enable Database Access", value=True)
    st.divider()
    st.markdown("### Recent Chats")
    st.caption("Sales Database Query")
    st.caption("Revenue Analysis")

# Header with Custom Interlocking Data Node Logo
st.markdown("""
<div class="header-container">
    <svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="15" y="15" width="30" height="30" rx="6" fill="#1E3A8A"/>
        <rect x="55" y="55" width="30" height="30" rx="6" fill="#3B82F6"/>
        <rect x="55" y="15" width="30" height="30" rx="6" fill="#93C5FD"/>
    </svg>
    <h1 class="title-text">Production Intelligence Agent</h1>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Chat with minimal letter block avatars ('U' and 'A')
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="U"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage) and msg.content:
        with st.chat_message("assistant", avatar="A"):
            st.write(msg.content)

if prompt := st.chat_input("Message the agent..."):
    user_msg = HumanMessage(content=prompt)
    st.session_state.messages.append(user_msg)
    
    with st.chat_message("user", avatar="U"):
        st.write(prompt)
    
    with st.chat_message("assistant", avatar="A"):
        trace_placeholder = st.empty()
        response_placeholder = st.empty()
        final_answer = ""
        
        try:
            inputs = {"messages": st.session_state.messages}
            with trace_placeholder.status("Processing workflow...", expanded=False) as status:
                for event in agent_executor.stream(inputs, stream_mode="updates"):
                    for node_name, state_update in event.items():
                        new_messages = state_update.get("messages", [])
                        for msg in new_messages:
                            if isinstance(msg, AIMessage) and msg.content:
                                final_answer = msg.content
                                st.session_state.messages.append(msg)
                status.update(label="Complete", state="complete", expanded=False)
            
            if final_answer:
                response_placeholder.write(final_answer)
                
        except Exception as e:
            st.error(f"Execution Error: {e}")