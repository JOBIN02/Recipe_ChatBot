import streamlit as st
import requests

st.set_page_config(page_title="🍳 Recipe Assistant", page_icon="🥘")

st.title("🍳 Recipe Assistant Chatbot")

# Keep conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What ingredients do you have? (e.g., Eggs, Onions)"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🍳"):
            try:
                response = requests.post(
                                "https://b5439872cdbf.ngrok-free.app/chat",  # 👈 use ngrok URL
                    json={"query": prompt}
                )

                ai_response = response.json().get("response", "⚠️ No response from server")
            except Exception as e:
                ai_response = f"❌ Error: {e}"

            st.markdown(ai_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
