import streamlit as st
import os
from dotenv import load_dotenv
from agent import build_agent

load_dotenv()

st.set_page_config(page_title="AI News Agent", page_icon="📰", layout="centered")
st.title("AI News Agent")
st.caption("Live AI news search, powered by LangChain + Groq + Tavily")

@st.cache_resource
def get_agent():
    return build_agent()

agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask about the latest AI news...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Searching...")
        full_text = ""
        for chunk in agent.stream(
            {"messages": st.session_state.messages},
            stream_mode="messages"
        ):
            msg = chunk[0]
            
            if "ai" in msg.type.lower() and msg.content:
                full_text += msg.content
                placeholder.markdown(full_text)
        answer = full_text
    st.session_state.messages.append({"role": "assistant", "content": answer})