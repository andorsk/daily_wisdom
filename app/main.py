# !/usr/bin/env python3

import yaml
import random
import os
import requests
from fastapi import FastAPI, HTTPException, Request
from typing import Optional
import json

global data
data = {}

app = FastAPI()

def build_slack_message(title, content):
    msg = {
	    "response_type": "in_channel",
            "blocks": [
                { "type": "section",
                  "text": {
                      "type": "mrkdwn",
		              "text":  "*{}*".format(title)
	       	 }},
                {
                  "type": "section",
		            "text": {
                  	    "type": "mrkdwn",
			            "text": '```' + content + '```'
		        }}
            ]
   	}
    return msg

def load_data(file):
    print("Opening ", file[1])
    with open(file[1], "r") as stream:
        try:
            global data
            data[file[0]] = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise
            print(exc)

@app.get("/quote")
async def get_quote(tags="famous-quotes"):
    params = {
        tags: tags
    }
    resp = requests.get("https://api.quotable.io/random", params=params)
    if resp.status_code == 200:
        return resp.json()
    raise ValueError("Got Response Code: {}".format(resp.status_code))

@app.get("/joke")
async def get_joke():
    global data
    key = "joke"
    i = random.randint(0, len(data[key])-1)
    if key not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    return data[key][i]

@app.post("/slack/joke")
async def get_slack_joke():
    try:
        d = await get_joke()
        return build_slack_message(d["setup"], d["punchline"])
    except Exception as e:
        raise e

@app.get("/fact")
async def get_fact():
    api_key = os.environ.get("X_API_KEY")
    headers = {
        "X-API-KEY": api_key
    }
    params = {"limit": 1}
    resp = requests.get(" https://api.api-ninjas.com/v1/facts", params=params, headers=headers)
    return resp.json()[0]["fact"]

@app.post("/slack/fact")
async def get_slack_fact():
    try:
        d = await get_fact()
        return build_slack_message("Random Fact", d)
    except Exception as e:
        raise e

@app.get("/{key}")
async def get_wisdom(key: str = "tao"):
    reserved = ["quote", "fact"]
    if key in reserved:
        raise ValueError("Routing error. Reserved")

    global data
    if key == 'favicon.ico':
       raise HTTPException(status_code=500, detail="Failure")
    i = random.randint(0, len(data[key])-1)
    if key not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    return data[key][i]

@app.post("/slack/quote")
async def get_slack_quote():
    try:
        d = await get_quote()
        response = {
	    "response_type": "in_channel",
            "blocks": [
                { "type": "section",
                  "text": {
                      "type": "mrkdwn",
		              "text": "*Random Quote: {}*".format(d.get("author", "Unknown Author"))
	       	 }},
                {
                  "type": "section",
		            "text": {
                  	    "type": "mrkdwn",
			            "text": '```' + d.get("content", "I seem to have forgotten my wisdom") + '```'
		        }}
            ]
   	}
        return response
    except Exception as e:
        raise e

@app.post("/slack/{key}")
async def get_wisdom_for_slack(key: str = "tao", request: Request = None):
    print("Got data {}".format(request))
    try:
        d = await get_wisdom(key)
        print("Got {}".format(d))
        response = {
	    "response_type": "in_channel",
            "blocks": [
                { "type": "section",
                  "text": {
                      "type": "mrkdwn",
		              "text": "*{}*".format(d.get("title", "Unknown Wisdom"))
	       	 }},
		 {
                  "type": "section",
		  "text": {
                  	"type": "mrkdwn",
			 "text": '```' + d.get("content", "I seem to have forgotten my wisdom") + '```'
		  }}
            ]
   	}
        return response
    except Exception as e:
        raise e


try:
    file = os.environ.get("DATAFILE", "./files.json")
    print("Opening", file)
    fdata = json.load(open(file, "r"))
    for f in fdata.items():
        load_data(f)
    print("Initialized")

except Exception as e:
    exit(1)


