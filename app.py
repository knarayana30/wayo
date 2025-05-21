import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
from openai import OpenAI

# Configure OpenAI client
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Page config
st.set_page_config(
    page_title="Wayo Travel Advisor",
    page_icon="✈️",
    layout="wide",
)

# Custom CSS for modern design
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        padding: 15px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        animation: fadeIn 0.5s;
    }
    .chat-message.user {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .chat-message.bot {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stSelectbox {
        background-color: rgba(255, 255, 255, 0.1);
    }
    .stSlider {
        color: white;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Header
st.title("✨ Wayo Travel Advisor")
st.markdown("---")

# Sidebar with travel preferences
with st.sidebar:
    st.header("🌍 Travel Preferences")
    budget = st.slider("💰 Budget (USD)", 0, 10000, 2000, 100)
    duration = st.slider("📅 Duration (Days)", 1, 30, 7)
    travel_style = st.selectbox(
        "🎯 Travel Style",
        ["Adventure", "Relaxation", "Cultural", "Luxury", "Budget"]
    )
    season = st.selectbox(
        "🌤️ Season",
        ["Summer", "Winter", "Spring", "Fall"]
    )

# Chat interface
st.markdown("### 💬 Chat with your Travel Assistant")

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
            <div class="chat-message user">
                <div>👤 You: {message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-message bot">
                <div>🤖 Wayo: {message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Ask me anything about travel recommendations!", key="user_input")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Wayo, a friendly and knowledgeable travel advisor. Keep responses concise and engaging."},
                {"role": "user", "content": f"""
                    Consider these preferences:
                    - Budget: ${budget}
                    - Duration: {duration} days
                    - Travel Style: {travel_style}
                    - Season: {season}
                    
                    Question: {user_input}
                """}
            ]
        )
        
        # Add bot response to chat history
        bot_response = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
        # Rerun to update chat display
        st.experimental_rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Wayo Travel")