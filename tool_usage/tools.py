WEATHER = {
    'moskow': 25,
    'london': 20,
    'miami': 18,
    'dubai': 30
}
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


def get_weather(city: str):
    return WEATHER[city.lower()]

def calculate_discount(price: int, status: str):
    return price * (DISCOUNT[status.lower()] / 100)

def get_from_db(id: int):
    return DB[id]