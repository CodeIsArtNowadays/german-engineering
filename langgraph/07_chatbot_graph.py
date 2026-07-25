from typing import TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from config import AI_KEY


llm = ChatOpenAI(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY,
    model='gpt-4.1-nano'
)


class AgentState(TypedDict):
    messages: list[HumanMessage | AIMessage]


def get_message_from_user_node(state: AgentState) -> AgentState:
    message = input('User message: ')
    state['messages'].append(HumanMessage(content=message))
    return state

def process_node(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    state['messages'].append(AIMessage(content=response.content))
    print('AI message: ' + response.content)
    return state

def decider_node(state: AgentState):
    last_message = state['messages'][-1]
    if last_message == 'stop':
        return 'stop'
    else:
        return 'llm'

graph = StateGraph(AgentState)
graph.add_node('chat', action=get_message_from_user_node)
graph.add_node('process', action=process_node)

graph.add_edge(START, 'chat')
graph.add_conditional_edges(
    source='chat',
    path=decider_node,
    path_map={
        'stop': END,
        'llm': 'process'
    }
)
graph.add_edge('process', 'chat')

app = graph.compile()
# with open("langgraph\\images\\07_graph_hw.png", "wb") as f:
#     f.write(app.get_graph().draw_mermaid_png())
app.invoke({'messages': []})