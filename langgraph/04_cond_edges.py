from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    x: int
    y: int
    operation: str
    final: str


def add_note(state: AgentState) -> AgentState:
    '''This node adds the 2 numbers'''
    state['final'] = state['x'] + state['y']
    return state

def multiply_node(state: AgentState) -> AgentState:
    '''This node multiply the 2 numbers'''
    state['final'] = state['x'] * state['y']
    return state

def decide_next_node(state: AgentState) -> AgentState:
    '''This node will choose next node of the graph'''

    if state['operation'] == '+':
        return 'addition_operation'
    elif state['operation'] == '*':
        return 'multiply_operation'


graph = StateGraph(AgentState)

graph.add_node('adder', add_note)
graph.add_node('multiplier', multiply_node)
graph.add_node('router', lambda state: state)

graph.add_edge(START, 'router')
graph.add_conditional_edges(
    source='router',
    path=decide_next_node,
    path_map={
        'addition_operation': 'adder',
        'multiply_operation': 'multiplier'
    }
)
graph.add_edge('adder', END)
graph.add_edge('multiplier', END)

app = graph.compile()

# with open("langgraph\\04_graph.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

initial_state = AgentState(x=5, y=5, operation='*')
res = app.invoke(initial_state)

print(res)