from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(docs, chunk_size=300, chunk_overlap=50):
    """Split documents into smaller overlapping chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)
