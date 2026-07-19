from graph.state import AgentState

from rag.utils.rag_chain import responder_con_rag
from database.utils.sql_chain import consultar_base_de_datos

def sql_node(state: AgentState) -> AgentState:
    question = state['question']
    
    respuesta = consultar_base_de_datos(question)
    
    return {
        **state,
        'answer':respuesta
    }
    
def rag_node(state: AgentState) -> AgentState:
    
    question = question = state['question']
    
    respuesta = responder_con_rag(question)
    
    return {
        **state,
        "are_docs": respuesta['are_docs'],
        "rag_success": respuesta['rag_success'],
        "docs": respuesta['docs'] if respuesta['docs'] else None,
        "answer": respuesta['answer'] if respuesta['answer'] else None,
        'final_action':'rag'
    }