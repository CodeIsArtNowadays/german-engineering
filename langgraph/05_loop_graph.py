from random import randint

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    name: str
    values: list[int]
    result: int | None
    finale: str


def greeting_node(state: AgentState) -> AgentState:
    state['finale'] = 'Hola, ' + state['name']
    return state

def rand_node(state: AgentState) -> AgentState:
    i = randint(0, 10)
    if i > 8:
        state['result'] = i
    state['values'].append(i)

    return state

def decide_random_node(state: AgentState) -> str:
    if state['result']:
        return 'end'
    else:
        return 'random_loop'


graph = StateGraph(AgentState)

graph.add_node('greeter', action=greeting_node)
graph.add_node('randomer', action=rand_node)


graph.add_edge(START, 'greeter')
graph.add_edge('greeter', 'randomer')
graph.add_conditional_edges(
    source='randomer',
    path=decide_random_node,
    path_map={
        'end': END,
        'random_loop': 'randomer'
    }
)

app = graph.compile()

with open("langgraph\\images\\05_graph.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())

init_state = AgentState(
    name='Jack Sparrow',
    values=[],
    result=None
)
result = app.invoke(init_state)
print(result)