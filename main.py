# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# load langchain modules
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from pypdf import PdfReader

# -------------------------------
# 1️⃣ Prepare your documents
# -------------------------------
pdf_file = open("sample-pdf.pdf", "rb")
read_pdf = PdfReader(pdf_file)
number_of_pages = len(read_pdf.pages)
texts = []

for page_number in range(number_of_pages):
    page = read_pdf.pages[page_number]
    page_content = page.extract_text()
    texts.append(page_content)

# Here we wrap each string inside a 'Document' object.
docs = [Document(page_content=t) for t in texts]


# -------------------------------
# 2️⃣ Split text into chunks
# -------------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# -------------------------------
# 3️⃣ Embed and store in memory
# -------------------------------
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vectorstore = InMemoryVectorStore(embeddings)
vectorstore.add_documents(chunks)


# Create retriever
# Convert the vector store into a retriever object.
# A retriever is responsible for finding the most relevant document chunks
# when you give it a user query (like "What is LangChain?").
# 
# The parameter 'search_kwargs' allows you to control how the retriever searches.
# Here, we pass {"k": 2}, which means:
# → For each query, return the top 2 most relevant text chunks from the vector store.
# 
# 'k' represents the number of documents (chunks) to fetch based on similarity.
# Increasing 'k' gives the model more context but can also add noise.
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


# -------------------------------
# 4️⃣ Build the RAG chain
# -------------------------------
prompt = ChatPromptTemplate.from_template("""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
""")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
parser = StrOutputParser()

def rag_answer(question: str):
    # 🔍 Step 1: Retrieve the most relevant chunks for the given question
    # The retriever searches the vector store and returns top-k matching Documents
    # Each Document contains text (page_content) that is semantically similar to the question
    retrieved_docs = retriever.invoke(question)

    # 🧩 Step 2: Combine all retrieved document texts into one big context string
    # This context will be fed to the LLM so it can ground its answer in real data
    # "\n\n" adds blank lines between chunks to separate them clearly
    context = "\n\n".join(d.page_content for d in retrieved_docs)

    # ⚙️ Step 3: Build a processing chain using LangChain's new Runnable syntax
    # The data flows through: prompt → llm → parser
    # - 'prompt' formats the question + context into a structured input
    # - 'llm' (like Gemini or GPT) generates the response
    # - 'parser' cleans or structures the output
    chain = prompt | llm | parser

    # 🚀 Step 4: Run the chain
    # Supply both the retrieved context and the user question to the pipeline
    # The model uses this information to produce a context-aware answer
    return chain.invoke({"context": context, "question": question})


# -------------------------------
# 5️⃣ Test the pipeline
# -------------------------------
if __name__ == "__main__":
    question = "what is res.send()?"
    answer = rag_answer(question)
    print("\nQuestion:", question)
    print("Answer:", answer)

