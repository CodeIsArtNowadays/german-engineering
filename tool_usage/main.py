import json

from openai import OpenAI

from config import AI_KEY 
from tool_schemas import tools, TOOLS_REGISTER


client = OpenAI(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY
)

prompts = [
    'user with id 3 got check on 600$, how much he pay with his discount',
    'weather in london',
    'hellow',
    'tell me about unicorns',
    'what is weather in moskow and london'
]

def main():
    messages=[{'role': 'user', 'content': 'what is weather in moskow and london or paris'}]
    has_tool_to_call = True

    while has_tool_to_call:
        response = client.chat.completions.create(
            model='gpt-4.1-nano',
            messages=messages,
            tools=tools  
        )
        message = response.choices[0].message
    
        messages.append(message)
    
        tool_calls = message.tool_calls
    
        if not tool_calls:
            has_tool_to_call = False
            continue
        
        for tool in message.tool_calls:
            func = TOOLS_REGISTER[tool.function.name]
            params = json.loads(tool.function.arguments)
            print(params)
            result = func(**params)
            print(result)
            messages.append({
                'role': 'tool',
                'tool_call_id': tool.id,
                'content': json.dumps(result)
            })
    return message.content

if __name__ == '__main__':
    print(main())