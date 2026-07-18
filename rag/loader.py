from langchain_community.document_loaders import (DirectoryLoader, TextLoader)

def get_docs():
    return DirectoryLoader("docs", 
                      loader_cls=TextLoader, 
                      glob="**/*.md",  
                      loader_kwargs={"encoding": "utf-8"} ).load()