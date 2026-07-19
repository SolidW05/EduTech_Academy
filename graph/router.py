from graph.state import AgentState

def arista_decision_triaje(state: AgentState) -> str:
    tri = state["decision"]

    if tri["route"] == "rag":
        return "rag"
    elif tri["route"] == "sql":
        return "sql"
    elif tri['route'] == 'hybrid':
        return 'hybrid'
    else:
        return "ask_info"

if __name__=='__main__':
    print(arista_decision_triaje({
        'decision': {
            'route':'hybrid'
        }
    }))