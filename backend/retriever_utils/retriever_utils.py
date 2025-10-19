def build_retriever(vectorstore, k=2):
    """Convert the vector store into a retriever that fetches top-k similar chunks."""
    return vectorstore.as_retriever(search_kwargs={"k": k})
