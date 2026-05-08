import streamlit as st
import google.generativeai as genai

# Access the secret securely from Streamlit's environment
# This replaces the manual text_input sidebar
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3-flash")
else:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

st.title("🤖 My Private Gemini AI")

# --- Rest of your chat code goes here ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})