from fastapi import HTTPException
from ..data import data
import random

async def get_wisdom(key: str):
    if key not in data or not data[key]:
        raise HTTPException(status_code=404, detail=f"Wisdom for '{key}' not found")
    return random.choice(data[key])
