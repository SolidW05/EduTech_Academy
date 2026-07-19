"""
app.py

Interfaz de Streamlit para mostrar el agente de LangGraph (rag / sql / hybrid / ask_info).

Notas importantes sobre el manejo del grafo:
- El grafo se compila con MemorySaver, que guarda el estado en memoria del PROCESO
  (no en disco). Por eso el grafo se construye UNA SOLA VEZ con @st.cache_resource:
  si lo reconstruyéramos en cada rerun de Streamlit, perderíamos el checkpoint y
  el hilo de conversación no podría "recordar" nada.
- El nodo `ask_info` usa `interrupt(...)`, lo que pausa la ejecución del grafo.
  Cuando eso pasa, `graph.stream(...)` entrega un chunk especial con la clave
  "__interrupt__". Detectamos esto, mostramos la pregunta de aclaración al
  usuario, y cuando responde, reanudamos el grafo con `Command(resume=respuesta)`
  usando el MISMO thread_id (config).
- Ajustá el import de `build_graph` de acuerdo a dónde vive realmente en tu proyecto.
"""

import uuid

import streamlit as st
from langgraph.types import Command

# --- Ajustá este import según la ubicación real de build_graph() en tu proyecto ---
from graph.graph import build_graph


st.set_page_config(page_title="Agente LangGraph", page_icon="🤖", layout="centered")


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
        st.session_state.messages = []  # [{"role": "user"/"assistant", "content": str, "route": str|None}]
    if "pending_interrupt" not in st.session_state:
        st.session_state.pending_interrupt = False


init_session()


def new_conversation():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.session_state.pending_interrupt = False


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuración")
    debug_mode = st.toggle("Modo debug (mostrar docs / artefactos)", value=False)
    st.caption(f"Thread ID:\n`{st.session_state.thread_id}`")
    if st.button("🔄 Nueva conversación", use_container_width=True):
        new_conversation()
        st.rerun()


st.title("🤖 Agente LangGraph")
st.caption("rag · sql · hybrid · ask_info")


# ---------------------------------------------------------------------------
# Lógica de invocación del grafo (usando .stream())
# ---------------------------------------------------------------------------
def run_graph(user_input: str, is_resume: bool):
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    stream_input = Command(resume=user_input) if is_resume else {"question": user_input}

    interrupt_question = None

    for chunk in graph.stream(stream_input, config=config, stream_mode="updates"):
        if "__interrupt__" in chunk:
            interrupt_obj = chunk["__interrupt__"][0]
            interrupt_question = interrupt_obj.value
            break

    if interrupt_question is not None:
        return {"type": "interrupt", "content": interrupt_question}

    # El grafo llegó a END (o volvió a esperar input): leemos el estado final
    final_state = graph.get_state(config).values
    return {
        "type": "final",
        "answer": final_state.get("answer"),
        "final_action": final_state.get("final_action"),
        "docs": final_state.get("docs"),
        "are_docs": final_state.get("are_docs"),
        "rag_success": final_state.get("rag_success"),
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
                st.json(msg["docs"])


# ---------------------------------------------------------------------------
# Input del usuario
# ---------------------------------------------------------------------------
placeholder = (
    "Respondé la aclaración pedida..."
    if st.session_state.pending_interrupt
    else "Escribí tu pregunta..."
)

if prompt := st.chat_input(placeholder):
    st.session_state.messages.append({"role": "user", "content": prompt, "route": None})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                result = run_graph(prompt, is_resume=st.session_state.pending_interrupt)
            except Exception as e:
                st.error(f"Error ejecutando el grafo: {e}")
                st.stop()

        if result["type"] == "interrupt":
            st.markdown(result["content"])
            st.session_state.messages.append(
                {"role": "assistant", "content": result["content"], "route": "ask_info"}
            )
            st.session_state.pending_interrupt = True
        else:
            answer = result.get("answer") or "_(el agente no devolvió una respuesta)_"
            st.markdown(answer)
            if result.get("final_action"):
                st.caption(f"Ruta: `{result['final_action']}`")
            if debug_mode and result.get("docs"):
                with st.expander("📄 Docs recuperados"):
                    st.json(result["docs"])

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "route": result.get("final_action"),
                    "docs": result.get("docs"),
                }
            )
            st.session_state.pending_interrupt = False