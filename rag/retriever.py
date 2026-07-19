from rag.vectorstore import get_vectorstore


def get_retriever():
    return get_vectorstore().as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5
    }
)