#!/usr/bin/env python3

import uvicorn
from fastapi import FastAPI
from app import routes
from app.utilities import init_logger, init_data

app = FastAPI()
app.include_router(routes.router)

if __name__ == "__main__":
    logger = init_logger()
    logger.info("Initializing")
    init_data(logger)
    logger.info("Starting server")
    uvicorn.run("main:app", port=5000, log_level="info")
