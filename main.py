# !/usr/bin/env python3
# Copyright (C) Benri.io - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Maintainer: andor
# Contact: andor@benri.io
# Date: 2022-04-07

import yaml
import argparse
import random
import os

global data
data = None

from fastapi import FastAPI

app = FastAPI()

def load_data(file):
    with open(file, "r") as stream:
        try:
            global data
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise
            print(exc)

@app.get("/tao")
def read_root():
    global data
    i = random.randint(0, len(data)-1)
    return data[i]


try:
    print("Loading data file")
    file = os.environ.get("DATAFILE", "tao.yml")
    load_data(file)
    print("Data is loaded")
except Exception as e:
    exit(1)
