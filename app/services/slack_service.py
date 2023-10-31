from .joke_service import get_joke
from .quote_service import get_quote
from .fact_service import get_fact
from .wisdom_service import get_wisdom

async def build_slack_message(title, content):
    return {
        "response_type": "in_channel",
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*{title}*"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": f'```{content}```'}}
        ]
    }

async def get_slack_joke():
    joke = await get_joke()
    return await build_slack_message(joke["setup"], joke["punchline"])

async def get_slack_quote():
    quote = await get_quote()
    author = quote.get("author", "Unknown Author")
    content = quote.get("content", "No quote found")
    return await build_slack_message(f"Random Quote: {author}", content)

async def get_slack_fact():
    fact = await get_fact()
    return await build_slack_message("Random Fact", fact)

async def get_slack_wisdom(key: str):
    wisdom = await get_wisdom(key)
    title = wisdom.get("title", "Unknown Wisdom")
    content = wisdom.get("content", "No wisdom found")
    return await build_slack_message
