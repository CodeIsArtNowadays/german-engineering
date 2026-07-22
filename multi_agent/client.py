from openai import Client
from config import AI_KEY


client = Client(
    base_url='https://api.proxyapi.ru/openai/v1',
    api_key=AI_KEY
)