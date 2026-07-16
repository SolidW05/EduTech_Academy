from langchain_community.document_loaders import (DirectoryLoader, TextLoader)
from langchain_text_splitters import MarkdownTextSplitter

mds = DirectoryLoader("docs", 
                      loader_cls=TextLoader, 
                      glob="**/*.md",  
                      loader_kwargs={"encoding": "utf-8"} ).load()
splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(mds)
len(chunks)