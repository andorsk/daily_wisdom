import logging
import json
import os
from .data import data

def init_logger():
    logger = logging.getLogger('gunicorn.error')
    logger.setLevel(logging.INFO)
    return logger

def init_data(logger):
    try:
        file = os.environ.get("DATAFILE", "./files.json")
        logger.info(f"Opening {file}")
        fdata = json.load(open(file, "r"))
        for f in fdata.items():
            load_data(f, logger)
        logger.info("Data initialized")
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        exit(1)

def load_data(file, logger):
    import yaml
    try:
        with open(file[1], "r") as stream:
            data[file[0]] = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logger.error(f"YAML error: {exc}")
        raise
