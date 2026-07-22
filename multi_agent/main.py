import json

from config import AI_KEY
from client import client
from db import Base, create_note, create_task, engine
from tools import get_curren_date, refactor_note, planner_agent_tools, editor_agent_tools


#
# Agent:
#   1. get_time, create task in db
#   2. format text, create task in db 
# DB:
#   1. task -> time, text


TOOLS_REGISTER = {
    'get_current_date': {
        'function': get_curren_date
    },
    'create_task': {
        'function': create_task
    },
    'create_note': {
        'function': create_note
    },
    'refactor_note': {
        'function': refactor_note
    }
}

def run_agent(system_prompt: str, user_prompt: str, tools: list[schema]):
    MAX_ITER = 10
    iteration = 0
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    has_tools_to_call = True

    while has_tools_to_call:
        iteration += 1
        if iteration > MAX_ITER:
            print('Max iter limit has reached')
            break

        response = client.chat.completions.create(
            model='gpt-4.1-nano',
            messages=messages,
            tools=tools
        )

        message = response.choices[0].message
        messages.append(message)

        tools_to_call = message.tool_calls

        if not tools_to_call:
            has_tools_to_call = False
            continue

        for tool in tools_to_call:
            func = TOOLS_REGISTER.get(tool.function.name)['function']
            params = json.loads(tool.function.arguments)
            print(func)
            print(params)
            result = func(**params)

            messages.append({
                'role': 'tool',
                'tool_call_id': tool.id,
                'content': json.dumps(result)
            })
    return message.content

def main():
    user_prompt = 'There’s a call with Oleg tomorrow at 12:00 about marketing. And make a note of this: it’s better to use short videos for ads—static images don’t work anymore.'
    planner_result = run_agent(
        system_prompt='You are planner helper. You need to extracts hard facts related to times, meetings, and tasks from a chaotic note, and save it to db. Use the %Y-%m-%d %H:%M:%S format in time stamps. you have a tool to get current date time',
        user_prompt=user_prompt,
        tools=planner_agent_tools
    )
    print('Planner agent result: ', planner_result)
    editor_result = run_agent(
        system_prompt='You are note taking helper. You need to extract valuable insights, ideas, and instructions from there, and organize them into a well-designed knowledge base, and save it to db. You cannot edit text on your own, you MUST use tool to refactor note before save it to db. Also do not repeat task that already was saved',
        user_prompt=planner_result,
        tools=editor_agent_tools
    )
    print('Editor agent result: ', editor_result)

    return 

def update_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    # update_db()
    # create_note('make multiagent mini app in 1h 30min')
    main()