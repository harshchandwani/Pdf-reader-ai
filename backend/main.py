# ==========================================
# 🚀 Main Script Entry
# ==========================================
import os
from dotenv import load_dotenv
load_dotenv()

# Read from .env (already loaded via load_dotenv)
MAX_PDF_SIZE_MB = int(os.getenv("MAX_PDF_SIZE_MB", 5))  # default 5 MB
MAX_PDF_SIZE = MAX_PDF_SIZE_MB * 1024 * 1024  # convert MB to bytes

from pydantic import BaseModel

from pdf_loader.pdf_loader import load_pdf
from text_splitter.text_splitter import split_documents
from vectorstore_utils.vectorstore_utils import create_vectorstore
from retriever_utils.retriever_utils import build_retriever
from rag_chain.rag_chain import build_rag_chain, rag_answer
from session_cleanup.session_cleanup import cleanup_sessions

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
from datetime import datetime
import asyncio

app = FastAPI(title="RAG PDF Q&A")

# ✅ Allowed frontend origins
origins = [
    os.getenv("FRONTEND_URL", "https://pdf-reader-fyafbbfus-harshchandwanis-projects.vercel.app"),   # Vite / React local dev
    os.getenv("FRONTEND_IP", "http://127.0.0.1:8080"),  # alternative local dev
    # Add your deployed frontend URL here when deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],            # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],            # Allow all headers
)

# In-memory storage for session_id -> vector store / chain
sessions = {}

@app.on_event("startup")
async def startup_event():
    # start background cleanup task
    asyncio.create_task(cleanup_sessions(sessions))

# 0️⃣ Add this near the top with your other endpoints

@app.get("/status")
async def status():
    """
    Simple health check endpoint.
    Returns a JSON confirming the API is running.
    """
    return {"status": "ok", "message": "RAG PDF API is running!"}

# 1️⃣ Upload PDF and create session
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Read file once
    contents = await file.read()

    # Check size
    if len(contents) > MAX_PDF_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"PDF size exceeds the limit of {MAX_PDF_SIZE_MB} MB"
        )

    # Save file
    temp_file = f"temp_{uuid.uuid4()}.pdf"
    with open(temp_file, "wb") as f:
        f.write(contents)
    # Process PDF → chunks → vector store → retriever → RAG chain
    docs = load_pdf(temp_file)
    chunks = split_documents(docs)
    vectorstore = create_vectorstore(chunks)
    retriever = build_retriever(vectorstore, k=2)
    chain = build_rag_chain()

    # Create session
    session_id = str(uuid.uuid4())
    # After saving your temporary file (example: temp_file = f"temp_{uuid.uuid4()}.pdf")
    sessions[session_id] = {
        "vectorstore": vectorstore,
        "retriever": retriever,
        "chain": chain,
        "last_active": datetime.now(),
        "pdf_path": temp_file  # 👈 store the temp PDF file path here
    }

    return JSONResponse({"session_id": session_id, "message": "PDF uploaded and processed"})


# Define request schema
class QueryRequest(BaseModel):
    session_id: str
    question: str

# 2️⃣ Ask query

@app.post("/query")
async def ask_query(request: QueryRequest):
    session_id = request.session_id
    question = request.question

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")


    # Update last activity
    sessions[session_id]["last_active"] = datetime.now()

    retriever = sessions[session_id]["retriever"]
    chain = sessions[session_id]["chain"]

    answer = rag_answer(question, retriever, chain)
    return {"answer": answer}
