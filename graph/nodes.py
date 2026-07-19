from graph.state import AgentState

from langchain_core.prompts import ChatPromptTemplate
from rag.utils.rag_chain import responder_con_rag
from database.utils.sql_chain import consultar_base_de_datos
from prompts.prompts import ROUTER_PROMPT, DENY_RESPONSE_PROMPT, CLARIFICATION_PROMPT
from ai_models.llm import LLMFactory
from pydantic import BaseModel
from typing import Literal
from langchain.agents import create_agent
from tools.rag_tool import *
from tools.sql_tool import *
from langchain_core.messages import ToolMessage
from langgraph.types import interrupt
from langchain_core.output_parsers import StrOutputParser


def format_history(history):
    return "\n".join(f"Usuario: {h['question']}\nAsistente: {h['answer']}" for h in history)


"""
Nodo de sql
""" 
def sql_node(state: AgentState) -> AgentState:
    question = state['question']
    history = format_history(state['history'])
    
    respuesta = consultar_base_de_datos(question, history)
    
    return {
        **state,
        'answer':respuesta,
        "history": [{"question": question, "answer": respuesta}]
    }
"""
Nodo del rag
""" 
def rag_node(state: AgentState) -> AgentState:
    
    question = state['question']
    history = format_history(state['history'])
    
    respuesta = responder_con_rag(question, history=history)
    
    return {
        **state,
        "are_docs": respuesta['are_docs'],
        "rag_success": respuesta['rag_success'],
        "docs": respuesta['docs'] if respuesta['docs'] else None,
        "answer": respuesta['answer'] if respuesta['answer'] else None,
        'final_action':'rag',
        "history": [{"question": question, "answer": respuesta}]
    }

"""
Nodo de decision
"""


class Route(BaseModel):
    route: Literal[
        "rag",
        "sql",
        "hybrid",
        "ask_info",
        "deny"]
    
def decision_node(state: AgentState) -> str:
    
    llm = LLMFactory.gemini()
    
    router_prompt = ChatPromptTemplate.from_messages([
    ("system", ROUTER_PROMPT),
    ("human", 
     "Historial de la conversación:\n{history}\n\n"
     "Pregunta actual del usuario:\n{question}")
])

    router_chain = (
        router_prompt
        | llm.with_structured_output(Route)
    )

    result = router_chain.invoke({
        "question": state["question"],
        "history": format_history(state.get("history", []))
    })
    
    return {**state,
        "decision": result.model_dump()}
    
"""
Nodo hybrid
"""   

# resultado = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "tienen cursos de python y cual es su precio y como los podria rembolsar?"
#             }
#         ]
#     }
# )


def hybrid_node(state: AgentState) -> AgentState:
    
    llm = LLMFactory.gemini()
    
    tools = [consultar_base_de_datos_tool, consultar_documentos]

    hybrid_agent = create_agent(
        
        model=llm,
        tools=tools
        
    )
    question =  state["question"]
    
    messages = []
    for h in state.get("history", []):
        messages.append(("human", h["question"]))
        messages.append(("ai", h["answer"]))
    messages.append(("human", state["question"]))

    resultado = hybrid_agent.invoke({"messages": messages})
    

    mensajes = resultado["messages"]
    respuesta_final = mensajes[-1].text
    
    tool_messages = [m for m in mensajes if isinstance(m, ToolMessage)]

    # en vez de un dict plano que se pisa, guardamos por nombre de tool
    artifacts_por_tool = {}
    for tm in tool_messages:
        if isinstance(tm.artifact, dict):
            artifacts_por_tool[tm.name] = tm.artifact

    rag_artifact = artifacts_por_tool.get("consultar_documentos")
    sql_artifact = artifacts_por_tool.get("consultar_base_de_datos")
    

    return {
        **state,
        **rag_artifact,
        #"rag_artifact": rag_artifact,   # puede ser None si no se llamó
        #"sql_artifact": sql_artifact,   # puede ser None si no se llamó
        "answer": respuesta_final,
        "final_action": "hybrid",
        "history": [{"question": question, "answer": respuesta_final}]
    }
'''
nodo ask info
'''



class ClarificationQuestion(BaseModel):
    question: str
    
clarification_prompt = ChatPromptTemplate.from_messages([
    ("system", CLARIFICATION_PROMPT),
    ("human", "{question}")
])



def ask_info_node(state: AgentState) -> AgentState:
    gemma = LLMFactory.gemma()

    clarification_chain = (
                    clarification_prompt |
                    gemma.with_structured_output(ClarificationQuestion) |
                    (lambda x: x.question)
                    )

    
    answer = interrupt(
        clarification_chain.invoke({'question':state['question']})
    )
    
    return {
        "question": (
            state["question"]
            + "\nInformación adicional: "
            + answer
        )
    }
"""
nodo de negacion
"""

def deny_node(state: AgentState) -> AgentState:
    
    llm = LLMFactory.gemma()
    
    deny_prompt = ChatPromptTemplate.from_messages([
    ("system", DENY_RESPONSE_PROMPT),
    ("human", '''
     Peticion del usuario:
     
     {question}
     ''')
    ])
    
    deny_chain = (
                deny_prompt |
                llm |
                StrOutputParser()
    )
    
    result = deny_chain.invoke({
        "question": state["question"]
    })
    
    return {
        **state,
        "answer": result,
        "final_action": "deny"
    }
    
    
    
    
    
if __name__=="__main__":
    print(hybrid_node({
        'question':'cuanto cuestan los cursos de python y como me podrian devolver el dinero si no me gustaron?'
    }))