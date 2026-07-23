import math

from typing import List, TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    values: List[int]
    name: str
    operation: str
    result: str


def process_values(state: AgentState) -> AgentState:
    '''This function process multiple different values'''

    match state['operation']:
        case '*':
            res = math.prod(state['values'])
        case '+':
            res = sum(state['values'])
        case _:
            print('unknown oprerator')
    state['result'] = f'Hi {state["name"]}, your sum - {res}'
    return state


graph = StateGraph(AgentState)

graph.add_node('processing_node', process_values)
graph.set_entry_point('processing_node')
graph.set_finish_point('processing_node')

app = graph.compile()

result = app.invoke({'values': [1, 2, 3, 4, 5], 'name': 'Robbert Paulsen', 'operation': '*'})

print(result)