from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ai_models.llm import LLMFactory
from prompts.prompts import SQL_RESPONSE_GENERATOR

response_prompt = ChatPromptTemplate.from_messages(
    SQL_RESPONSE_GENERATOR
)

llm = LLMFactory.gemini()


sql_response_generator =(
    response_prompt | llm | StrOutputParser()
)