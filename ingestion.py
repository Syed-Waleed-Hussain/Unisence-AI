import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


DATA_PATH = "data/"
DB_PATH = "chroma_db/"

def build_vector_pipeline():
    # Verify if the data directory exists and contains files
    if not os.path.exists(DATA_PATH) or not os.listdir(DATA_PATH):
        print(f"Error: Directory '{DATA_PATH}' is empty or does not exist.")
        return

    print("Status: Initializing data ingestion process...")

    documents = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            print(f"Status: Loading document: {file}")
            try:
                loader = PyPDFLoader(os.path.join(DATA_PATH, file))
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {file}: {e}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, 
        chunk_overlap=80
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Status: Document splitting complete. Total chunks created: {len(chunks)}")

    # Load the embedding model (converts text to numbers)
    print("Status: Loading embedding model. This may take a moment...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create and save the vector database
    print("Status: Generating vector database...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print(f"Success: Vector database has been saved to '{DB_PATH}'.")
    print("Status: Pipeline execution completed successfully.")

if __name__ == "__main__":
    build_vector_pipeline()
