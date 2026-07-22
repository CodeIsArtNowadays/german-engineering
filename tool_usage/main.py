import json

from openai import OpenAI
from pydantic import ValidationError

from config import AI_KEY
from tool_schemas import tools
from tools import get_from_db, get_weather, calculate_discount
from schemas import GetWeatherToolArg, GetFromDbToolArg, CalculateDiscountToolArg

client = OpenAI(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY
)

TOOLS_REGISTER = {
    'get_weather': {
        'function': get_weather,
        'args_schema': GetWeatherToolArg
    },
    'get_from_db': {
        'function': get_from_db, 
        'args_schema': GetFromDbToolArg
    },
    'calculate_discount': {
        'function': calculate_discount,
        'args_schema': CalculateDiscountToolArg
    }
}

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
    MAX_ITER = 10
    iteration = 0
    while has_tool_to_call:
        iteration += 1
        if iteration > MAX_ITER:
            print('Limit operations has been reached')
            break
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
            tool_entry = TOOLS_REGISTER.get(tool.function.name)
            if not tool_entry:
                result = {'error': f'tool {tool.tool.function.name} is not registred'}
            else:
                func = tool_entry['function']
                param_schema = tool_entry['args_schema']
                try:
                    params = param_schema(**json.loads(tool.function.arguments))
                except (json.JSONDecodeError, ValidationError) as e:
                    result = {'error': e}
                else:
                    try:
                        result = func(**params.model_dump())
                    except Exception as e:
                        result = {'error': f'tool failed: {e}'}
            messages.append({
                'role': 'tool',
                'tool_call_id': tool.id,
                'content': json.dumps(result)
            })
    return message.content

if __name__ == '__main__':
    print(main())
