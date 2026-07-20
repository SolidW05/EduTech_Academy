
from rag.utils.rag_chain import responder_con_rag
from langchain_core.tools import tool


@tool(response_format="content_and_artifact")
def consultar_documentos(pregunta: str, history: str) -> str:
    """Útil para responder preguntas sobre contenido descriptivo de los cursos:
    temarios, descripciones, metodología, requisitos, contenido de clases, etc.
    Usa esta herramienta cuando la pregunta sea conceptual o abierta, no cuando pida
    un dato exacto de la base de datos.
    recibe dos argumentos, y en este orden:
    pregunta: la pregunta del usuario (str)
    history: el historial de la conversacion (messages) (str)
    """
    
    resultado = responder_con_rag(pregunta, history)
    
    content = resultado.pop('answer')
    
    artifact = resultado
    
    
    
    return content , artifact