import requests
import os
from fastapi import HTTPException

async def get_fact():
    api_key = os.environ.get("X_API_KEY")
    headers = {"X-API-KEY": api_key}
    params = {"limit": 1}
    try:
        response = requests.get("https://api.api-ninjas.com/v1/facts", params=params, headers=headers)
        response.raise_for_status()
        return response.json()[0]["fact"]
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
