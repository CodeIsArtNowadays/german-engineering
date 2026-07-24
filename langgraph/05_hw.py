from random import randint

from typing import TypedDict
from langgraph.graph import StateGraph, END, START


class AgentState(TypedDict):
    player: str
    target: int | None
    guesses: list[int]
    attemps: int
    lower_bound: int
    upper_bound: int
    

def setup_node(state: AgentState) -> AgentState:
    state['target'] = randint(1, 100)
    return state

def guess_node(state: AgentState) -> AgentState:
    guess = int((state['lower_bound'] + state['upper_bound']) / 2)
    state['guesses'].append(guess)
    state['attemps'] += 1
    return state

def hint_node(state: AgentState) -> AgentState:
    print(state)
    last_guess = state['guesses'][-1]
    target = state['target']
    if last_guess == target:
        return state
    else: 
        if last_guess > target:
            state['upper_bound'] = last_guess - 1
        elif last_guess < target:
            state['lower_bound'] = last_guess + 1
        return state

def decider(state: AgentState):
    if state['guesses'][-1] == state['target'] or state['attemps'] > 7:
        return 'end'
    else:
        return 'loop'
    

graph = StateGraph(AgentState)

graph.add_node('setup', action=setup_node)
graph.add_node('guess', action=guess_node)
graph.add_node('hint', action=hint_node)

graph.add_edge(START, 'setup')
graph.add_edge('setup', 'guess')
graph.add_edge('guess', 'hint')
graph.add_conditional_edges(
    source='hint',
    path=decider,
    path_map={
        'end': END,
        'loop': 'guess'
    }
)


app = graph.compile()


# with open("langgraph\\images\\05_graph_hw.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())

init_state = AgentState(
    player='Me',
    guesses=[],
    target=None,
    attemps=0,
    lower_bound=1,
    upper_bound=100
)

result = app.invoke(init_state)
print(result)