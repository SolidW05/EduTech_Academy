"""
app.py

Interfaz de Streamlit para mostrar el agente de LangGraph (rag / sql / hybrid / ask_info)
de EduTech Academy.

Notas sobre el manejo del grafo:
- El grafo se compila con MemorySaver, que guarda el estado en memoria del PROCESO
  (no en disco). Por eso se construye UNA SOLA VEZ con @st.cache_resource: si se
  reconstruyera en cada rerun de Streamlit, se perdería el checkpoint y el hilo de
  conversación no podría "recordar" nada.
- El nodo `ask_info` usa `interrupt(...)`, lo que pausa la ejecución del grafo.
  En vez de detectar la interrupción parseando los chunks del stream (formato que
  puede variar entre versiones de LangGraph), usamos `graph.get_state(config)`
  como única fuente de verdad:
    - `snapshot.next`                -> si no está vacío, el grafo quedó pausado
    - `snapshot.tasks[i].interrupts` -> el valor de la interrupción pendiente
  Esto evita el bug de "el primer mensaje de respuesta no hace nada": antes
  dependíamos de un flag manual que podía desincronizarse del estado real del
  grafo (por ejemplo si `decision` volvía a rutear a `ask_info` una segunda vez).
- Ajustá el import de `build_graph` según dónde vive en tu proyecto.
"""

import uuid

import streamlit as st
from langgraph.types import Command

# --- Ajustá este import según la ubicación real de build_graph() en tu proyecto ---
from graph.graph import build_graph


st.set_page_config(page_title="Agente EduTech Academy", page_icon="🎓", layout="centered")


# ---------------------------------------------------------------------------
# Construcción del grafo (una sola vez para todo el proceso)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_graph():
    return build_graph()


graph = get_graph()


# ---------------------------------------------------------------------------
# Estado de sesión
# ---------------------------------------------------------------------------
def init_session():
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []  # [{"role", "content", "route"?, "docs"?}]


init_session()


def new_conversation():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []


config = {"configurable": {"thread_id": st.session_state.thread_id}}


# ---------------------------------------------------------------------------
# Helpers de estado del grafo (fuente única de verdad sobre interrupts)
# ---------------------------------------------------------------------------
def is_graph_paused() -> bool:
    """True si el grafo quedó esperando un resume (ej. interrupt en ask_info)."""
    return bool(graph.get_state(config).next)


def get_pending_interrupt_text():
    snapshot = graph.get_state(config)
    for task in snapshot.tasks:
        if task.interrupts:
            return task.interrupts[0].value
    return None


pending_interrupt = is_graph_paused()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuración")
    debug_mode = st.toggle("Modo debug (mostrar docs recuperados)", value=False)
    st.caption(f"Thread ID:\n`{st.session_state.thread_id}`")
    if st.button("🔄 Nueva conversación", use_container_width=True):
        new_conversation()
        st.rerun()


# ---------------------------------------------------------------------------
# Encabezado + qué puede preguntar el usuario
# ---------------------------------------------------------------------------
st.title("🎓 Agente EduTech Academy")

with st.expander("❓ ¿Qué puedo preguntar?", expanded=(len(st.session_state.messages) == 0)):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📄 Políticas y documentación**")
        st.markdown(
            "- Reglamento del estudiante\n"
            "- Cómo usar la plataforma\n"
            "- Becas\n"
            "- Reembolsos\n"
            "- Privacidad\n"
            "- Términos y condiciones\n"
            "- Preguntas frecuentes\n"
            "- Certificados\n"
            "- Soporte técnico\n"
            "- Catálogo académico"
        )
    with col2:
        st.markdown("**🗄️ Datos académicos**")
        st.markdown(
            "- Cursos: precio, duración, nivel, cupos\n"
            "- Categorías de cursos\n"
            "- Instructores y su especialidad\n"
            "- Inscripciones y progreso\n"
            "- Becas otorgadas\n"
            "- Certificados emitidos"
        )
    st.caption(
        "Ejemplos: «¿cuál es la política de reembolsos?» · "
        "«¿cuánto cuesta el curso de Python y cuántos cupos quedan?» · "
        "«¿cómo verifico si un certificado es válido?»"
    )


# ---------------------------------------------------------------------------
# Render "lindo" de documentos recuperados (en vez de st.json crudo)
# ---------------------------------------------------------------------------
def _get(obj, *keys, default=None):
    """Busca el primer campo disponible, tanto en dict como en atributos de objeto."""
    for key in keys:
        if isinstance(obj, dict) and obj.get(key) not in (None, ""):
            return obj[key]
        if hasattr(obj, key) and getattr(obj, key) not in (None, ""):
            return getattr(obj, key)
    return default


def render_docs(docs):
    if not docs:
        st.caption("No se recuperaron documentos.")
        return

    for i, doc in enumerate(docs, start=1):
        content = _get(doc, "page_content", "content", "text", default=str(doc))
        metadata = _get(doc, "metadata", default={}) or {}
        source = _get(doc, "source") or (
            metadata.get("source") if isinstance(metadata, dict) else None
        )
        score = _get(doc, "score") or (
            metadata.get("score") if isinstance(metadata, dict) else None
        )
        source_name = source.replace("\\", "/").split("/")[-1] if source else f"Fragmento {i}"

        with st.container(border=True):
            header = f"📄 **{source_name}**"
            if score is not None:
                try:
                    header += f"  ·  relevancia: {float(score):.2f}"
                except (TypeError, ValueError):
                    pass
            st.markdown(header)
            preview = content if len(content) <= 500 else content[:500] + "…"
            st.markdown(preview)


# ---------------------------------------------------------------------------
# Invocación del grafo (con .stream())
# ---------------------------------------------------------------------------
def run_graph(user_input: str, is_resume: bool):
    stream_input = Command(resume=user_input) if is_resume else {"question": user_input}

    for _ in graph.stream(stream_input, config=config, stream_mode="updates"):
        pass  # consumimos todo el stream; el estado se lee después con get_state

    # `snapshot.next` es la ÚNICA fuente de verdad de si el grafo quedó
    # pausado (es el mismo chequeo que is_graph_paused()). No alcanza con
    # mirar si get_pending_interrupt_text() devolvió texto: si por lo que
    # sea `tasks[i].interrupts` viene vacío aunque el grafo SÍ esté
    # pausado, esta rama caía al "final_state" de abajo y devolvía una
    # respuesta vacía -> el interrupt se "perdía" en ese mensaje y recién
    # se resolvía con el próximo (que sí se mandaba como resume, porque
    # is_graph_paused() detectaba bien el estado pausado). De ahí el
    # patrón de "tengo que mandar un mensaje y después otro".
    if is_graph_paused():
        pending = get_pending_interrupt_text()
        return {
            "type": "interrupt",
            "content": pending or "Necesito un poco más de información para continuar. ¿Podrías dar más detalles?",
        }

    final_state = graph.get_state(config).values
    return {
        "type": "final",
        "answer": final_state.get("answer"),
        "final_action": final_state.get("final_action"),
        "docs": final_state.get("docs"),
    }


# ---------------------------------------------------------------------------
# Render del historial
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("route"):
            st.caption(f"Ruta: `{msg['route']}`")
        if debug_mode and msg.get("docs"):
            with st.expander("📄 Docs recuperados"):
                render_docs(msg["docs"])


# ---------------------------------------------------------------------------
# Input del usuario
# ---------------------------------------------------------------------------
placeholder = "Respondé la aclaración pedida..." if pending_interrupt else "Escribí tu pregunta..."

if prompt := st.chat_input(placeholder):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                result = run_graph(prompt, is_resume=pending_interrupt)
            except Exception as e:
                st.error(f"Error ejecutando el grafo: {e}")
                st.stop()

        if result["type"] == "interrupt":
            st.markdown(result["content"])
            st.session_state.messages.append(
                {"role": "assistant", "content": result["content"], "route": "ask_info"}
            )
        else:
            answer = result.get("answer") or "_(el agente no devolvió una respuesta)_"
            st.markdown(answer)
            if result.get("final_action"):
                st.caption(f"Ruta: `{result['final_action']}`")
            if debug_mode and result.get("docs"):
                with st.expander("📄 Docs recuperados"):
                    render_docs(result["docs"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "route": result.get("final_action"),
                    "docs": result.get("docs"),
                }
            )