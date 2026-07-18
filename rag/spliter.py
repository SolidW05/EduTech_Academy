from langchain_text_splitters import MarkdownTextSplitter
from loader import get_docs

splitter = MarkdownTextSplitter(chunk_size=1000, 
                                chunk_overlap=100)

def get_chunks():
    
    docs = get_docs()
    return splitter.split_documents(docs)