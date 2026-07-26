from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from config import AI_KEY


DISCOUNT = {
    'gold': 50,
    'silver': 25,
    'bronze': 10
}
DB = {
    1: {'name': 'Belka', 'discount_status': 'silver'},
    2: {'name': 'Monroe', 'discount_status': 'bronze'},
    3: {'name': 'Black', 'discount_status': 'bronze'},
    4: {'name': 'White', 'discount_status': 'gold'},
    5: {'name': 'Pink', 'discount_status': 'silver'},
    6: {'name': 'Orange', 'discount_status': 'silver'},
}

@tool
def calculate_discount(price: int, status: str):
    '''calculate discount based on discount status'''
    return price * (DISCOUNT[status.lower()] / 100)

@tool
def get_from_db(user_id: int):
    '''Get user information from db. Returns name and discount status'''
    return DB[user_id]



class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

tools = [calculate_discount, get_from_db]
llm = ChatOpenAI(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY,
    model='gpt-4.1-mini'
).bind_tools(tools)

def ask_llm(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=
        'You are my AI assistant, please answer my query to the best of your ability.'
    )
    response = llm.invoke([system_prompt] + state['messages'])
    
    return {'messages': [response]} 

def decider_node(state: AgentState):
    print('\n\n\n', state['messages'])
    messages = state['messages']
    last_message = messages[-1]
    if not last_message.tool_calls:
        return 'end'
    else:
        return 'continue'


graph = StateGraph(AgentState)
graph.add_node('agent', action=ask_llm)
tool_node = ToolNode(tools=tools)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'agent')
graph.add_conditional_edges(
    source='agent',
    path=decider_node,
    path_map={
        'continue': 'tools',
        'end': END
    }
)
graph.add_edge('tools', 'agent')
app = graph.compile()

init_state = AgentState({'messages': 'how much should user 1 pay after applying the discount on 1000$ check'})
app.invoke(init_state)