import streamlit as st
import requests

# 🚀 Backend API URL (your FastAPI server / ngrok / cloud endpoint)
BACKEND_URL = "http://127.0.0.1:8000/query"   # change to your deployed backend URL

st.set_page_config(page_title="Recipe Assistant", page_icon="🍳", layout="centered")

st.title("🍳 Recipe Assistant Chatbot")
st.write("Enter ingredients or a recipe query, and I'll suggest matching recipes!")

# Input box
query = st.text_input("🔍 What ingredients or recipe would you like to search for?", "")

# Submit button
if st.button("Find Recipes"):
    if query.strip() == "":
        st.warning("Please enter a query (like 'eggs and onions').")
    else:
        try:
            # Call FastAPI backend
            response = requests.post(BACKEND_URL, json={"query": query})
            
            if response.status_code == 200:
                answer = response.json().get("response", "No response")
                st.success("✅ Recipe Suggestion:")
                st.write(answer)
            else:
                st.error(f"⚠️ Error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Could not connect to backend: {e}")
