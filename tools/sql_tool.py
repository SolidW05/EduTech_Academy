from database.utils.sql_chain import consultar_base_de_datos
from langchain_core.tools import tool


@tool
def consultar_base_de_datos_tool(pregunta: str, history: str) -> str:
    """Útil para responder preguntas sobre datos estructurados y exactos de EduTech Academy:
    precios de cursos, instructores por categoría/tema, cantidad de estudiantes inscritos,
    certificados emitidos, fechas de inscripción, etc.
    Usa esta herramienta cuando la pregunta pida un dato concreto que vive en la base de datos
    (números, nombres, fechas, listados).
    recibe dos argumentos, y en este orden:
    pregunta: la pregunta del usuario (str)
    history: el historial de la conversacion (messages) (str)
    """
    return consultar_base_de_datos(pregunta, history)