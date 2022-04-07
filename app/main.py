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
from fastapi import FastAPI
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
def read_root(key: str):
    global data
    i = random.randint(0, len(data)-1)
    return data[key][i]

try:
    file = os.environ.get("DATAFILE", "./files.json")
    print("Opening", file)
    fdata = json.load(open(file, "r"))
    for f in fdata.items():
        load_data(f)
    print("Initialized")
except Exception as e:
    exit(1)
