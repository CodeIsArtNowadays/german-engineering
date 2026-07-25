from typing import TypedDict
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START

from config import AI_KEY


class AgentState(TypedDict):
    messages: list[HumanMessage]


llm = ChatOpenAI(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY,
    model='gpt-4.1-mini'
)

def process_node(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    print(response.content)
    return state

graph = StateGraph(AgentState)
graph.add_node('process', action=process_node)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

app = graph.compile()
init_state = AgentState(
    messages=[HumanMessage(content='tell me about unicorns'),]
)
app.invoke(init_state)


