from typing import TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState) -> AgentState:
    '''Simple node that add a greeting message to the state'''

    state['message'] = 'Hey ' + state['message']
    return state

def comlimenting_node(state: AgentState) -> AgentState:
    '''add Compliment to a state'''
    state['message'] = state['message'] + '! Nice to see you'
    return state
    
graph = StateGraph(AgentState)  # ty:ignore[invalid-argument-type]
graph.add_node('greeter_node', action=greeting_node)
graph.add_node('complimenter_node', action=comlimenting_node)
graph.set_entry_point('greeter_node')
graph.add_edge('greeter_node', 'complimenter_node')
graph.set_finish_point('complimenter_node')

app = graph.compile()

result = app.invoke({'message': 'Bob'})  # ty:ignore[invalid-argument-type]

print(result['message'])