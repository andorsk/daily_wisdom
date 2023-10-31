from ..data import data
from fastapi import HTTPException
import random

async def get_joke():
    key = "joke"
    if key not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    i = random.randint(0, len(data[key])-1)
    return data[key][i]
