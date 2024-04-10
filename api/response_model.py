from pydantic import BaseModel
from typing import List


class StrikePriceRequest(BaseModel):
    strike_price: int

class OptionData(BaseModel):
    option_type: str
    data: List[dict]
