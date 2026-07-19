from config import AI_KEY

from openai import OpenAI


client = OpenAI(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY
)

response = client.chat.completions.create(
    model='gpt-4.1-nano',
    messages=[{'role': 'user', 'content': 'tell me about unicorns'}]
)

print(response.choices[0].message.content)