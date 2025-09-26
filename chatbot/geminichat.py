import streamlit as st
import google.generativeai as genai

# Configure Gemini API key (store it in Streamlit secrets like before)
genai.configure(api_key="o")

st.title("Streaming Gemini Chat Clone 😉🔭💬")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

if prompt := st.chat_input("Wassup write smth here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream Gemini response
    with st.chat_message("assistant"):
        response = st.write_stream(
            model.start_chat(
                history=[
                    {"role": m["role"], "parts": [m["content"]]}
                    for m in st.session_state.messages
                ]
            ).send_message(prompt, stream=True)
        )

    st.session_state.messages.append({"role": "assistant", "content": response})


