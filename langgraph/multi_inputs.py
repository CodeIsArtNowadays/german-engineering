from typing import List, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str


def process_values(state: AgentState) -> AgentState:
    '''This function process multiple different values'''
    state['result'] = f'Hi {state["name"]}, your sum - {sum(state["values"])}'

    return state


graph = StateGraph(AgentState)

graph.add_node('processing_node', process_values)
graph.set_entry_point('processing_node')
graph.set_finish_point('processing_node')

app = graph.compile()

result = app.invoke({'values': [1, 2, 3], 'name': 'Robbert Paulsen'})

print(result)