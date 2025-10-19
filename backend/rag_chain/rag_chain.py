from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def build_rag_chain():
    """Create a pipeline (prompt → llm → parser)."""
    prompt = ChatPromptTemplate.from_template("""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
""")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    parser = StrOutputParser()
    return prompt | llm | parser


def rag_answer(question: str, retriever, chain):
    """Retrieve relevant chunks, build context, and generate a grounded answer."""
    retrieved_docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in retrieved_docs)
    return chain.invoke({"context": context, "question": question})
