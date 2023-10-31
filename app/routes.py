from fastapi import APIRouter, HTTPException
from .services import joke_service, quote_service, fact_service, wisdom_service, slack_service

router = APIRouter()

@router.get("/quote")
async def get_quote(tags="famous-quotes"):
    return await quote_service.get_quote(tags)

@router.get("/joke")
async def get_joke():
    return await joke_service.get_joke()

@router.post("/slack/joke")
async def get_slack_joke():
    return await slack_service.get_slack_joke()

@router.get("/fact")
async def get_fact():
    return await fact_service.get_fact()

@router.post("/slack/fact")
async def get_slack_fact():
    return await slack_service.get_slack_fact()

@router.get("/{key}")
async def get_wisdom(key: str = "tao"):
    return await wisdom_service.get_wisdom(key)

@router.post("/slack/quote")
async def get_slack_quote():
    return await slack_service.get_slack_quote()

@router.post("/slack/{key}")
async def get_wisdom_for_slack(key: str = "tao"):
    return await slack_service.get_wisdom_for_slack(key)
