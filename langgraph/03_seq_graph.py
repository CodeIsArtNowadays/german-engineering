from typing import TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    age: str
    skills: list[str]
    final: str


def greeting_node(state: AgentState) -> AgentState:
    '''This is node to handle name'''

    state['final'] = 'Hi, ' + state['name']
    return state

def ageing_node(state: AgentState) -> AgentState:
    '''This is node to handle age'''

    state['final'] = state['final'] + f', you are {state['age']} age old'
    return state

def skill_node(state: AgentState) -> AgentState:
    '''This if node to handle skill set'''
    state['final'] += ', '.join(state['skills'])
    return state

graph = StateGraph(AgentState)

graph.add_node('greater', action=greeting_node)
graph.add_node('age', action=ageing_node)
graph.add_node('skill', action=skill_node)

graph.set_entry_point('greater')
graph.add_edge('greater', 'age')
graph.add_edge('age', 'skill')
graph.set_finish_point('skill')

app = graph.compile()

with open("langgraph\\graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

result = app.invoke({'name': 'Robbert Paulsen', 'age': '50', 'skills': ['python', 'backend', 'ai intergracion']})
print(result)