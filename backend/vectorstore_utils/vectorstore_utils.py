from langchain_core.vectorstores import InMemoryVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def create_vectorstore(chunks):
    """Embed the chunks using Gemini embeddings and store them in memory."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = InMemoryVectorStore(embeddings)
    vectorstore.add_documents(chunks)
    return vectorstore
