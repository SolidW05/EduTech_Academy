from rag.retriever import get_retriever
from rag.utils.rag_rewriter_chain import rag_rewriter_chain
from ai_models.llm import LLMFactory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = LLMFactory.gemini()

retriever = get_retriever()

rag_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Eres el asistente oficial de EduTech Academy.

Tu única fuente de información es el contexto proporcionado.

Responderás preguntas de estudiantes utilizando únicamente la información contenida en la documentación oficial.

Reglas:

- Responde únicamente con información presente en el contexto.
- No inventes políticas, fechas, procesos o requisitos.
- Si el contexto no contiene suficiente información para responder correctamente, indícalo claramente.
- Si existen varios fragmentos relevantes, intégralos en una única respuesta coherente.
- No menciones que utilizaste documentos o un sistema RAG.
- Mantén un tono profesional y claro.

Contexto:

{context}
"""
    ),
    (
        "human",
        "{question}"
    )
])

rag_chain = (
    rag_prompt
    | llm
    | StrOutputParser()
)

def responder_con_rag(pregunta: str) -> str:

    rag_rewritten_question = rag_rewriter_chain.invoke({"question": pregunta})

    docs_original = retriever.invoke(pregunta)
    docs = retriever.invoke(rag_rewritten_question)

    if not docs_original and not docs:
        return {
            "are_docs": False,
            "rag_success": False
        }

    context = f"""
    === Documentos encontrados con la pregunta original ===
    {chr(10).join(f"Documento: {d.metadata.get('source')}\n{d.page_content}" for d in docs_original)}

    === Documentos encontrados con la pregunta reescrita ===
    {chr(10).join(f"Documento: {d.metadata.get('source')}\n{d.page_content}" for d in docs)}
    """

    answer = rag_chain.invoke({
        "context": context,
        "question": f"pregunta original: {pregunta}, pregunta reescrita: {rag_rewritten_question}"
    })
    
    return  {
        "are_docs": True,
        "rag_success": True,
        "docs": docs + docs_original,
        "answer": answer
    }
    
if __name__=='__main__':
    print(responder_con_rag('cual es el proceso de devolucion de un curso?'))