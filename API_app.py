import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # We use a simple write() with the stream to keep it ultra-fast
        def stream_text():
            response = client.models.generate_content_stream(
                model="gemini-2.0-flash-lite",
                contents=prompt
            )
            for chunk in response:
                yield chunk.text

        # This built-in Streamlit function is the fastest way to show a stream
        full_text = st.write_stream(stream_text())
        st.session_state.messages.append({"role": "assistant", "content": full_text})
