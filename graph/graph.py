from graph.state import AgentState
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver

from graph.nodes import *

from graph.router import arista_decision_triaje


def build_graph():
    memory = MemorySaver()

    workflow = StateGraph(AgentState, start_state=START, end_state=END)
    workflow.add_node('rag', rag_node)
    workflow.add_node('decision', decision_node)
    workflow.add_node('sql', sql_node)
    workflow.add_node('hybrid', hybrid_node)
    workflow.add_node('ask_info', ask_info_node)

    workflow.add_edge(START, 'decision')
    workflow.add_conditional_edges("decision", arista_decision_triaje, {
        'rag':'rag',
        'hybrid':'hybrid',
        'sql':'sql',
        'ask_info':'ask_info'
    })
    workflow.add_edge('ask_info', 'decision')
    workflow.add_edge("rag", END)
    return workflow.compile(
        checkpointer=memory
    )