from typing import TypedDict
from langgraph.graph import StateGraph, END, START


class AgentState(TypedDict):
    n1: int
    n2: int
    n3: int
    n4: int
    operation1: str
    operation2: str
    final1: int | None
    final2: int | None


def add_node(state: AgentState) -> AgentState:
    '''Node to add two numbers'''
    if not state['final1']:
        state['final1'] = state['n1'] + state['n2']
    else:
        state['final2'] = state['n3'] + state['n4']
    return state

def substruct_node(state: AgentState) -> AgentState:
    '''Node to add substruct numbers'''
    if not state['final1']:
        state['final1'] = state['n1'] - state['n2']
    else:
        state['final2'] = state['n3'] - state['n4']
    return state

def decide_next_node(state: AgentState) -> str:
    '''Decide next node based on state'''
    if state['operation1'] == '+':
        return 'addition_operation'
    elif state['operation1'] == '-':
        return 'substraction_operation'

def decide_next_node2(state: AgentState) -> str:
    '''Decide next node based on state'''
    if state['operation2'] == '+':
        return 'addition_operation'
    elif state['operation2'] == '-':
        return 'substraction_operation'

graph = StateGraph(AgentState)

graph.add_node('adder1', action=add_node)
graph.add_node('substractor1', action=substruct_node)
graph.add_node('adder2', action=add_node)
graph.add_node('substractor2', action=substruct_node)

graph.add_node('router1', lambda state: state)
graph.add_node('router2', lambda state: state)

graph.add_edge(START, 'router1')
graph.add_conditional_edges(
    source='router1',
    path=decide_next_node,
    path_map={
        'addition_operation': 'adder1',
        'substraction_operation': 'substractor1'
    }
)
graph.add_edge('adder1', 'router2')
graph.add_edge('substractor1', 'router2')
graph.add_conditional_edges(
    source='router2',
    path=decide_next_node2,
    path_map={
        'addition_operation': 'adder2',
        'substraction_operation': 'substractor2'
    }
)
graph.add_edge('adder2', END)
graph.add_edge('substractor2', END)

app = graph.compile()

with open("langgraph\\images\\04_1_1_graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

initial_state = AgentState(
    n1=100,
    n2=5,
    n3=20,
    n4=7,
    operation1='+',
    operation2='-',
    final1=None,
    final2=None
)

result = app.invoke(initial_state)
print(result)
