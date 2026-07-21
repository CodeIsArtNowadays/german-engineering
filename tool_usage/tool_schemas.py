from tools import get_from_db, get_weather, calculate_discount


tools = [
{
    'type': 'function',
    'function': {
        'name': 'get_weather',
        'description': 'Return the weather in given city now',
        'strict': True,
        'parameters': {
            'type': 'object',
            'properties': {
                'city': {'type': 'string'}
            },
            'required': ['city'],
            'additionalProperties': False
        }
    }
},
{
    'type': 'function',
    'function': {
        'name': 'get_from_db',
        'description': 'Return user model from db. Fields on user model: name, discount_status',
        'strict': True,
        'parameters': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'}
            },
            'required': ['id'],
            'additionalProperties': False
        }
    }
},
{
    'type': 'function',
    'function': {
        'name': 'calculate_discount',
        'description': 'Calculate discount to price based on discount status',
        'strict': True,
        'parameters': {
            'type': 'object',
            'properties': {
                'price': {'type': 'integer'},
                'status': {'type': 'string'},
            },
            'required': ['price', 'status'],
            'additionalProperties': False
        }
    }
},

]

TOOLS_REGISTER = {
    'get_weather': get_weather,
    'get_from_db': get_from_db,
    'calculate_discount': calculate_discount
}