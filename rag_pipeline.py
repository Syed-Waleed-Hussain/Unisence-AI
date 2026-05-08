import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()

print("Loading embeddings...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print("Connecting to ChromaDB...")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 3}) 

print("Initializing Gemini...")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3) 

# 1. PICHLA SAWAL SAMAJHNE WALA LOGIC (Standalone Query Generator)
condense_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given the following chat history and the latest user question, rephrase the user question to be a standalone question. If it is already standalone, return it as is. Do not answer it."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])
condense_chain = condense_prompt | llm | StrOutputParser()

def get_standalone_query(x):
    # Agar chat history hai, toh purane sawalon ke reference se sawal poora karo
    if x.get("chat_history"):
        return condense_chain.invoke({"chat_history": x["chat_history"], "input": x["input"]})
    else:
        return x["input"]

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 2. MAIN ANSWER WALA PROMPT
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are 'UniSense AI', an intelligent assistant for university affairs at FAST NUCES.\nUse the following context to answer the question. If you don't know, say so.\n\nContext: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# 3. MODERN LCEL PIPELINE (Bina kisi langchain.chains import ke!)
rag_chain = (
    RunnablePassthrough.assign(
        standalone_query=lambda x: get_standalone_query(x)
    )
    | RunnablePassthrough.assign(
        context=lambda x: format_docs(retriever.invoke(x["standalone_query"]))
    )
    | qa_prompt
    | llm
    | StrOutputParser()
)

# --- LIVE CHAT LOOP ---
if __name__ == "__main__":
    chat_history = [] 

    print("\n" + "="*50)
    print("--- UniSense AI Ready (Type 'exit' to quit) ---")
    print("="*50 + "\n")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ['exit', 'quit']:
            print("UniSense AI: Good Bye! Turning off.")
            break

        # RAG chain ko run karna
        response = rag_chain.invoke({
            "input": user_query,
            "chat_history": chat_history
        })
        
        print(f"\nUniSense AI: {response}\n")
        print("-" * 50)

        # Agli baari ke liye history update karna
        chat_history.extend([
            HumanMessage(content=user_query),
            AIMessage(content=response)
        ])