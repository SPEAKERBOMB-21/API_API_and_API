import streamlit as st
from google import genai

# Setup the Gemini Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages from history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Accept new user input
if prompt := st.chat_input("Say something..."):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Generate assistant response with a live stream
    with st.chat_message("assistant"):
        
        # 1. Define the generator function
        def stream_text():
            # FIX: Use simple string for contents to match the new SDK format
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=prompt
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text

        # 2. FIX: Use st.write_stream to make it visually type out live on screen!
        full_response = st.write_stream(stream_text())
        
    # Add the final assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})


