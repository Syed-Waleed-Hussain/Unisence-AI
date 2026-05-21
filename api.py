from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import logging

# We import from rag_pipeline
from rag_pipeline import rag_chain
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="UniSense AI API")

# Add CORS middleware to allow requests from Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Streamlit on any port)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatRequest(BaseModel):
    input: str
    chat_history: List[Dict[str, str]] = [] # list of {"role": "human"|"ai", "content": "..."}

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        # Reconstruct chat_history objects for Langchain
        lc_chat_history = []
        for msg in req.chat_history:
            if msg.get("role") == "human":
                lc_chat_history.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "ai":
                lc_chat_history.append(AIMessage(content=msg.get("content", "")))

        response_text = rag_chain.invoke({
            "input": req.input,
            "chat_history": lc_chat_history
        })
        return ChatResponse(response=response_text)
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
