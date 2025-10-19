# ==========================================
# 🚀 Main Script Entry
# ==========================================
from dotenv import load_dotenv
load_dotenv()

from pdf_loader.pdf_loader import load_pdf
from text_splitter.text_splitter import split_documents
from vectorstore_utils.vectorstore_utils import create_vectorstore
from retriever_utils.retriever_utils import build_retriever
from rag_chain.rag_chain import build_rag_chain, rag_answer


def main():
    # 1️⃣ Load and prepare documents
    docs = load_pdf("sample-pdf.pdf")

    # 2️⃣ Split into chunks
    chunks = split_documents(docs)

    # 3️⃣ Embed and store in memory
    vectorstore = create_vectorstore(chunks)

    # 4️⃣ Build retriever
    retriever = build_retriever(vectorstore, k=2)

    # 5️⃣ Build RAG pipeline
    chain = build_rag_chain()

    # 6️⃣ Ask question
    question = "What is res.send()?"
    answer = rag_answer(question, retriever, chain)

    print("\nQuestion:", question)
    print("Answer:", answer)


if __name__ == "__main__":
    main()
