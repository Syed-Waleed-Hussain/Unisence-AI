import os
import logging
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['transformers_logging_level'] = 'error'
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("langchain").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "chroma_db"

def run_test_query():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

    query = "What happend if student's CGPA is lower than 2.0?"
    
    results = vector_db.similarity_search(query, k=2)

    print("\n" + "="*50)
    print("SEARCH RESULTS")
    print("="*50)

    if results:
        for i, doc in enumerate(results):
            cleaned_text = " ".join(doc.page_content.split())
            print(f"\nSection {i+1}:")
            print(cleaned_text)
            print("-" * 50)
    else:
        print("\nNo results found.")

if __name__ == "__main__":
    run_test_query()