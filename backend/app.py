import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/example")
async def example():
    return {"message": 'Hello'}
