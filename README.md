# 🎓 UniSense AI - Intelligent University Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green)
![Gemini](https://img.shields.io/badge/AI-Google_Gemini_2.5_Flash-orange)

UniSense AI is a state-of-the-art conversational agent designed for **FAST NUCES**. It utilizes a sophisticated Retrieval-Augmented Generation (RAG) pipeline to accurately answer student queries regarding university policies, fee structures, and curriculum guidelines by reading directly from official university PDF documents.

## ✨ Key Features
* **Intelligent Document Retrieval:** Uses ChromaDB and HuggingFace embeddings to search through university handbooks instantly.
* **Conversational Memory:** Remembers chat history and reformulates follow-up questions for flawless context-aware interactions.
* **Voice Interaction:** Speak to the AI using your microphone (`SpeechRecognition`) and listen to its responses via Text-to-Speech (`gTTS`).
* **Hallucination Prevention:** Strictly prompted to answer *only* from the retrieved FAST NUCES context.
* **Decoupled Architecture:** A high-performance backend via FastAPI bridged with an interactive Streamlit frontend.

## 🛠️ Tech Stack
* **LLM Engine:** Google Gemini 2.5 Flash
* **Orchestration:** LangChain (LCEL)
* **Vector Database:** ChromaDB
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
* **Backend:** FastAPI, Uvicorn, Pydantic
* **Frontend:** Streamlit
* **Voice Capabilities:** PyAudio, SpeechRecognition, gTTS

---

## 🚀 Installation & Setup Guide

### 1. Prerequisites
* Python 3.10 or higher.
* **Windows Users:** To utilize the Voice features, you *must* have [Microsoft Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed with the **"Desktop development with C++"** workload checked (Required for compiling `PyAudio`).

### 2. Clone the Repository
```
git clone [https://github.com/yourusername/UniSense_AI.git](https://github.com/yourusername/UniSense_AI.git)
cd UniSense_AI
```
### 3. Create a Virtual Environment
```
python -m venv venv

Activate the environment:

Windows: .\venv\Scripts\activate

Mac/Linux: source venv/bin/activate
```
### 4. Install Dependencies
Make sure your virtual environment is active, then run:

```
pip install -r requirements.txt
```
(If you face a PyAudio installation error on Windows, ensure C++ Build Tools are installed, or temporarily disable voice features in app.py).

### 5. Environment Variables
Create a file named .env in the root directory and add your Google Gemini API key:

```
GOOGLE_API_KEY="your_api_key_here"
```
### 6. Data Ingestion (First Time Only)
Place your university PDF documents inside the data/ folder, then run the ingestion script to build the vector database:

```
python ingestion.py
```
### 💻 How to Run the Application
You need two separate terminal windows to run the decoupled system.

Terminal 1: Boot up the Backend Server
Activate your environment and start the FastAPI server:

```
python api.py
```
The API will start running on http://localhost:8000.

Terminal 2: Launch the Frontend Interface
Open a new terminal, activate the environment, and start Streamlit:

```
streamlit run app.py
```
Your browser will automatically open UniSense AI at http://localhost:8501.

### 📂 Project Structure

UniSense_AI/
│
├── data/                   # Place official university PDFs here
├── chroma_db/              # Auto-generated vector database
├── api.py                  # FastAPI backend server
├── app.py                  # Streamlit frontend UI
├── ingestion.py            # PDF data extraction & vectorization script
├── rag_pipeline.py         # Core LangChain RAG & Memory engine
├── requirements.txt        # Project dependencies
└── .env                    # API keys (Not tracked in Git)
### 👥 Contributors
Developed for FAST NUCES Academic Project:

Syed Waleed Hussain (Core AI & RAG Pipeline Engine)

Sofia (Data Ingestion & Vector Database Architecture)

Huzaifa (FastAPI Backend Integration & Streamlit UI)
