from typing import TypedDict, Annotated, Sequence

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from config import AI_KEY


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


document_content = ''

@tool
def update(content: str) -> str:
    '''Update the document with the provided content.'''
    global document_content
    document_content += content
    return f'Document has been updated successfully! The current content is: \n {document_content}'

@tool
def save(filename: str) -> str:
    '''Save the current document to a text file and finish the process

    Agrs:
        filename: Name for the text file
    '''

    global document_content
    if not filename.endswith('.txt'):
        filename += '.txt'

    try:
        with open(filename, 'w') as file:
            file.write(document_content)
        print(f'\n Document has been saved to: {filename}')
        return 'Document has been saved successfully'
    except Exception as e:
        return f'Error while saving document: {str(e)}'

tools = [save, update]

llm = ChatOpenAI(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY,
    model='gpt-4.1-mini'
).bind_tools(tools)


def agent_node(state: AgentState):
    system_prompt = SystemMessage(content=f"""
        You are Drafter, a helpful writting assistant. You are going to help the user update and modify documents.
        - If the user wants to update or modify content, use the 'update' tool with the complete updated content. You should only pass the content from user input that meant to be added
        - If the user wants to save and finish, you need to user the 'save' tool.
        - Make sure to always show the current dociment state after modification
       The current document content is: {document_content}  
        """)

    if not state['messages']:
        user_input = 'What you would like to create'
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input('\nWhat would you like to do with this document?\n')
        user_message = HumanMessage(content=user_input)

    all_messages = [system_prompt] + list(state['messages']) + [user_message]
    response = llm.invoke(all_messages)
    return {'messages': list(state['messages']) + [user_message, response]}
    
def decider_node(state: AgentState):
    messages = state['messages']

    if not messages:
        return 'continue'

    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and
            'saved' in message.content.lower() and
            'document' in message.content.lower()
        ):
            return 'end'
    return 'continue'


graph = StateGraph(AgentState)
graph.add_node('agent', action=agent_node)
graph.add_node('tools', ToolNode(tools))

graph.add_edge(START, 'agent')
graph.add_edge('agent', 'tools')
graph.add_conditional_edges(
    source='tools',
    path=decider_node,
    path_map={
        'continue': 'agent',
        'end': END
    }
)

app = graph.compile()

app.invoke({'messages': []})
