import streamlit as st
import requests
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import base64
from analytics_db import get_total_queries, get_frequent_words, get_recent_queries

# Configuration
API_URL = "http://127.0.0.1:8000/chat"
ADMIN_PASSWORD = "admin"  

st.set_page_config(page_title="UniSense AI", page_icon="🎓", layout="centered")

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        fp.close() # Windows requires the file handle to be closed first
        tts.save(fp.name)
        
        # Give streamit the audio element
        with open(fp.name, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
            
        try:
            os.remove(fp.name)
        except PermissionError:
            pass 
    except Exception as e:
        st.error(f"TTS Error: {e}")

def recognize_speech():
    r = sr.Recognizer()
    # It attempts to use the default microphone
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        audio_data = r.listen(source, timeout=5, phrase_time_limit=15)
        st.info("Processing...")
        try:
            text = r.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.warning("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "ai", "content": "Hello! I'm UniSense AI, your intelligent assistant for university affairs at FAST NUCES. How can I help you today?"})

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "Admin Dashboard"])

    if page == "Chat":
        st.title("🎓 UniSense AI")
        st.caption("Your intelligent FAST NUCES assistant")

        # Download Chat History feature
        if len(st.session_state.messages) > 1:
            chat_text = "UniSense AI Chat History\n\n"
            for msg in st.session_state.messages:
                role = "User" if msg["role"] == "human" else "UniSense AI"
                chat_text += f"{role}: {msg['content']}\n\n"
            
            st.sidebar.download_button(
                label="📥 Download Chat History",
                data=chat_text,
                file_name="unisense_chat_history.txt",
                mime="text/plain"
            )

        # Display chat history
        for msg in st.session_state.messages:
            with st.chat_message("user" if msg["role"] == "human" else "assistant"):
                st.markdown(msg["content"])

        # Create a row for Voice and Text inputs
        # But st.chat_input is sticky to bottom, buttons aren't.
        # We can add a voice input button in the sidebar or at the bottom.
        if st.sidebar.button("🎤 Voice Input"):
            voice_text = recognize_speech()
            if voice_text:
                st.session_state.current_voice_input = voice_text

        # Using a session state variable to bridge voice input to chat
        current_input = st.chat_input("Type your message here...")
        
        # Check if we have voice input pending
        if hasattr(st.session_state, 'current_voice_input'):
            current_input = st.session_state.current_voice_input
            del st.session_state.current_voice_input
            
        if current_input:
            # 1. Show user message
            st.session_state.messages.append({"role": "human", "content": current_input})
            with st.chat_message("user"):
                st.markdown(current_input)
            
            # 2. Call FastAPI
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    payload = {
                        "input": current_input,
                        "chat_history": st.session_state.messages[:-1] # excludes current msg
                    }
                    try:
                        res = requests.post(API_URL, json=payload)
                        if res.status_code == 200:
                            response_text = res.json().get("response", "No response.")
                            st.markdown(response_text)
                            st.session_state.messages.append({"role": "ai", "content": response_text})
                            
                            # Log query directly from Streamlit or by Fast API. 
                            # Since we want to use the analytics DB
                            from analytics_db import log_query
                            log_query(current_input, response_text)

                            # TTS
                            if st.sidebar.checkbox("🔊 Enable Text-to-Speech", value=True):
                                text_to_speech(response_text)
                        else:
                            st.error(f"Error {res.status_code}: {res.text}")
                    except Exception as e:
                        st.error(f"Failed to connect to backend: {e}")

    elif page == "Admin Dashboard":
        st.title("Admin Dashboard")
        pwd = st.text_input("Enter Admin Password", type="password")
        if pwd == ADMIN_PASSWORD:
            st.success("Authenticated Successfully.")
            
            total_queries = get_total_queries()
            st.metric("Total Queries Handled", total_queries)
            
            st.subheader("Frequent Words/Topics")
            frequent_words = get_frequent_words()
            if frequent_words:
                col1, col2 = st.columns(2)
                for idx, (word, count) in enumerate(frequent_words):
                    if idx % 2 == 0:
                        col1.write(f"- **{word}**: {count} times")
                    else:
                        col2.write(f"- **{word}**: {count} times")
            else:
                st.write("No queries yet.")
                
            st.subheader("Recent Queries")
            recent = get_recent_queries(5)
            for r in recent:
                st.write(f"[{r['timestamp'][:16]}] {r['query']}")
                
        elif pwd:
            st.error("Incorrect Password.")

if __name__ == "__main__":
    from analytics_db import init_db
    init_db()
    main()
