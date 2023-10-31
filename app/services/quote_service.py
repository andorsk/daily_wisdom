import requests
from fastapi import HTTPException

async def get_quote(tags="famous-quotes"):
    params = {tags: tags}
    try:
        response = requests.get("https://api.quotable.io/random", params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
