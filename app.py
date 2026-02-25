import streamlit as st
import requests
import subprocess
import time
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Tour Planner AI",
    page_icon="✈️",
    layout="centered",
)


# --- AUTO-START FASTAPI BACKEND ---
@st.cache_resource
def start_backend():
    """Starts the FastAPI server in the background if it's not already running."""
    try:
        # Check if API is already alive
        requests.get("http://127.0.0.1:8000/", timeout=1)
    except:
        # If not, start it
        process = subprocess.Popen(
            ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(5)  # Give it time to boot
        return process


# This will trigger once when the app loads
start_backend()

# --- MINIMAL CSS ---
st.markdown(
    """
<style>
    .stApp {
        background-color: #ffffff;
    }
    .main-title {
        font-weight: 700;
        font-size: 2.5rem;
        color: #1a1a1a;
        margin-bottom: 0px;
    }
    .stChatMessage {
        border: 1px solid #f0f0f0;
        border-radius: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-title">TOUR PLANNER</h1>', unsafe_allow_html=True)
st.caption("AI-powered travel assistant for Nepal.")
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 Welcome! How can I help you plan your trip today?",
        }
    ]


def render_assistant_response(output):
    """Clean, linear rendering for clarity"""
    if isinstance(output, str):
        st.write(output)

    elif isinstance(output, dict) and isinstance(output.get("response"), list):
        data = output
        days = data.get("response", [])

        st.subheader(data.get("title", "Your Itinerary"))

        for day in days:
            with st.expander(
                f"📍 Day {day.get('day')}: {day.get('title')}", expanded=True
            ):
                st.markdown("**Schedule**")
                for item in day.get("schedule", []):
                    st.write(f"- {item}")

                st.markdown("**Accommodation**")
                st.info(day.get("hotel") or "No specific hotel information.")

                st.markdown("**Transport**")
                for t in day.get("transport", []):
                    st.write(f"- {t}")

        if data.get("confirmation"):
            st.success(f"❓ {data.get('confirmation')}")

    elif isinstance(output, dict) and "status" in output:
        if output.get("status") == "success":
            st.success(
                f"✅ **Booking Confirmed!**\n\n{output.get('message')}\n\n**ID:** `{output.get('booking_id')}`\n\n📞 *Our agency will call you shortly to finalize the arrangements.*"
            )
        else:
            st.error(output.get("message"))
    else:
        st.json(output)


# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        render_assistant_response(message["content"])

# User input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/user-1/classify",
                json={"user_query": prompt},
                timeout=60,
            )
            response.raise_for_status()
            api_data = response.json()
            assistant_response = api_data.get("response")
        except Exception as e:
            assistant_response = f"⚠️ Error: {e}"

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )
    with st.chat_message("assistant"):
        render_assistant_response(assistant_response)
