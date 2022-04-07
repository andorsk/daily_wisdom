# !/usr/bin/env python3
# Copyright (C) Benri.io - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Maintainer: andor
# Contact: andor@benri.io
# Date: 2022-04-07

import yaml
import random
import os
from fastapi import FastAPI, HTTPException, Request
from typing import Optional
import json

global data
data = {}

app = FastAPI()

def load_data(file):
    print("Opening ", file[1])
    with open(file[1], "r") as stream:
        try:
            global data
            data[file[0]] = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise
            print(exc)

@app.get("/{key}")
async def get_wisdom(key: str = "tao"):
    print("Got key: {}".format(key))
    global data
    i = random.randint(0, len(data[key])-1)
    if key not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    return data[key][i]

@app.post("/slack/{key}")
async def get_widsom_for_slack(key: str = "tao", request: Request = None):  
    print("Got data {}".format(request))
    try:
        d = await get_wisdom(key)
        print("Got {}".format(d))
        response = {
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
			     "text": d.get("content", "I seem to have forgotten my wisdom")
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


