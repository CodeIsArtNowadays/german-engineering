from pydantic import BaseModel


class GetWeatherToolArg(BaseModel):
    city: str

class GetFromDbToolArg(BaseModel):
    id: int

class CalculateDiscountToolArg(BaseModel):
    price: int
    