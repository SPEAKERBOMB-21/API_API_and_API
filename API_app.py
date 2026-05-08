import streamlit as st
from google import genai

st.set_page_config(page_title="SPEAKERBOMB AI", page_icon="🔊")
st.title("🔊 SPEAKERBOMB AI")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your speaker build..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        def stream_text():
            try:
                # Using the most stable 2026 configuration
                response = client.models.generate_content_stream(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                yield f"Connection hiccup! Just a second... (Error: {str(e)})"

        full_text = st.write_stream(stream_text())
    
    st.session_state.messages.append({"role": "assistant", "content": full_text})
