import json

from openai import OpenAI

from config import AI_KEY  
from tool_schemas import tools, TOOLS_REGISTER


client = OpenAI(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY
)

messages=[{'role': 'user', 'content': 'what is weather in london'}]

has_tool_to_call = True

while has_tool_to_call:
    response = client.chat.completions.create(
        model='gpt-4.1-nano',
        messages=messages,  # pyright: ignore[reportArgumentType]
        tools=tools  # pyright: ignore[reportArgumentType]
    )
    message = response.choices[0].message

    messages.append(message)



    for tool in message.tool_calls:
        func = TOOLS_REGISTER[tool.function.name]
        params = json.loads(tool.function.arguments)
        print(params)
        result = func(**params)

        message.append({
            'role': 'tool',
            'tool_call_id': tool.id,
            'content': json.dumps(result)
        })

    response = client.chat.completions.create(
        model='gpt-4.1-nano',
        messages=messages, 
        tools=tools  
    )
    print(response.choices[0].message.content)
    has_tool_to_call = False