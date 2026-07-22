from datetime import datetime

from client import client


planner_agent_tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_current_date',
            'description': 'Return the current date. Call with NO arguments',
            'strict': True,
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'create_task',
            'description': 'Creating task in database. Returns a created task if was created successfully',
            'strict': True,
            'parameters': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string'},
                    'time': {'type': 'string'}
                },
                'required': ['description', 'time'],
                'additionalProperties': False
            }
        }
    },
]

editor_agent_tools = [
    {
        'type': 'function',
        'function': {
            'name': 'create_note',
            'description': 'Creating note in database. Returns a created note if was created successfully',
            'strict': True,
            'parameters': {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string'},
                },
                'required': ['description'],
                'additionalProperties': False
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'refactor_note',
            'description': 'Refactor given text into a note-like format.',
            'strict': True,
            'parameters': {
                'type': 'object',
                'properties': {
                    'text': {'type': 'string'},
                },
                'required': ['text'],
                'additionalProperties': False
            }
        }
    }
]

def get_curren_date():
    return str(datetime.now())

def refactor_note(text: str):
    response = client.chat.completions.create(
        model='gpt-4.1-nano',
        messages=[
            {'role': 'system', 'content': 'You are smart note taker. You should refactor given text into well-structured note. Extract basic theses and represent it in 3-4 sentences semanticaly right. FORMAT OUTPUT: strict json object with 1 field named text. EXAMPLE \n {"description": "lorem ipsum val"}'}
        ]
    )
    return response.choices[0].message.content