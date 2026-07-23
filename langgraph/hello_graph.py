from typing import TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    message: str


def greeting_node(state: AgentState) -> AgentState:
    '''Simple node that add a greeting message to the state'''

    state['message'] = 'Hey ' + state['message']
    return state

graph = StateGraph(AgentState)  # ty:ignore[invalid-argument-type]
graph.add_node('greeter_node', action=greeting_node)
graph.set_entry_point('greeter_node')
graph.set_finish_point('greeter_node')

app = graph.compile()

result = app.invoke({'message': 'Bob'})  # ty:ignore[invalid-argument-type]

print(result['message'])