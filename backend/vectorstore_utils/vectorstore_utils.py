import os
from dotenv import load_dotenv
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load .env file (if you're using one)
load_dotenv()

def create_vectorstore(chunks):
    """Embed the chunks using Gemini embeddings and store them in memory."""
    # Make sure API key is loaded
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Please add it to your .env file.")

    # Initialize embeddings with the API key
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )

    # Create vector store in memory
    vectorstore = InMemoryVectorStore(embeddings)
    vectorstore.add_documents(chunks)

    return vectorstore
