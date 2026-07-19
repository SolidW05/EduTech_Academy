
from rag.utils.rag_chain import responder_con_rag
from langchain_core.tools import tool


@tool(response_format="content_and_artifact")
def consultar_documentos(pregunta: str) -> str:
    """Útil para responder preguntas sobre contenido descriptivo de los cursos:
    temarios, descripciones, metodología, requisitos, contenido de clases, etc.
    Usa esta herramienta cuando la pregunta sea conceptual o abierta, no cuando pida
    un dato exacto de la base de datos."""
    
    resultado = responder_con_rag(pregunta)
    
    content = resultado.pop('answer')
    
    artifact = resultado
    
    
    
    return content , artifact