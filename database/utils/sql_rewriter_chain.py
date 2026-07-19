from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from prompts.prompts import SQL_QUERY_REWRITER_PROMPT
from ai_models.llm import LLMFactory

class SQLQuery(BaseModel):
    sql: str

llm = LLMFactory.cohere()

sql_rewriter_prompt = ChatPromptTemplate.from_messages([
    ("system", SQL_QUERY_REWRITER_PROMPT),
    ("human", "Historial de la conversación:\n{history}\n\nPregunta actual:\n{question}")
])

sql_rewriter_chain = (
    sql_rewriter_prompt
    | llm.with_structured_output(SQLQuery)
    | (lambda x: x.sql)
)