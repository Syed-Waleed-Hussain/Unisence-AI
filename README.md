# 🎓 UniSense AI

UniSense AI is an intelligent, voice-enabled assistant designed to help students with university affairs at FAST NUCES. It utilizes a Retrieval-Augmented Generation (RAG) pipeline to deliver accurate and context-aware responses.

## ✨ Features

- **Conversational AI Interface:** A modern, ChatGPT-style UI built with Streamlit.
- **Voice Integration (Speech-to-Text & Text-to-Speech):** Speak your questions using your microphone and hear the AI's responses out loud at the click of a button.
- **Advanced RAG Pipeline:** Powered by LangChain, ChromaDB, HuggingFace Embeddings, and Google's Gemini LLM to process and query university-specific data.
- **RESTful Backend API:** A robust FastAPI backend bridging the core AI logic to the frontend via HTTP.
- **Admin Analytics Dashboard:** A password-protected dashboard to track query metrics, frequent keywords, and recent questions using SQLite.

## 🛠️ Technology Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI, Uvicorn
- **AI & Machine Learning:** LangChain, Google Gemini (LLM), HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Database:** ChromaDB
- **Voice Capabilities:** `SpeechRecognition`, `gTTS` (Google Text-to-Speech)
- **Database (Analytics):** SQLite3

---

## 🚀 How to Run the Project Locally

### 1. Prerequisites

Ensure you have **Python 3.10+** installed on your system.

### 2. Setup the Environment

1. Extract the project folder and open a Terminal / Command Prompt inside the folder.
2. Create an isolated virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

### 3. Install Dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a file named `.env` in the root directory and add your API keys:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Start the Application

You will need to open **two separate terminal windows** (ensure the virtual environment is activated in both).

**Terminal 1: Start the Backend (FastAPI)**

```bash
python api.py
```

_(The backend will start running on port 8000)._

**Terminal 2: Start the Frontend (Streamlit)**

```bash
streamlit run app.py
```

_(The frontend will automatically open in your default web browser at `http://localhost:8501`)._

---

## 📊 Admin Dashboard

To access the analytics dashboard:

1. Open the sidebar in the Streamlit app.
2. Select **Admin Dashboard**.
3. Enter the default password: **`admin`**
4. View metrics like total queries, frequently asked questions, and recent interaction logs.

## 📱 Mobile Testing

Because the frontend and backend are configured to run locally (with FastAPI serving `0.0.0.0` or `127.0.0.1`), you can access the app from your mobile device by typing your computer's local Wi-Fi IP address followed by `:8501` in your phone's browser (Make sure your phone and laptop are on the same Wi-Fi network). Ensure `API_URL` in `app.py` is dynamically set to handle this if you desire remote connections.
