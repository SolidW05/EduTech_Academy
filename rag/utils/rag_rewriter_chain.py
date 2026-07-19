from prompts.prompts import RAG_QUERY_REWRITER_PROMPT
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from ai_models.llm import LLMFactory

llm = LLMFactory.cohere()



class RAGQuery(BaseModel):
    question: str


rag_query_rewriter_prompt = ChatPromptTemplate.from_messages([
    ("system", RAG_QUERY_REWRITER_PROMPT),
    ("human", "{question}")
])


rag_rewriter_chain = (
    rag_query_rewriter_prompt
    | llm.with_structured_output(RAGQuery)
    | (lambda x: x.question)
)