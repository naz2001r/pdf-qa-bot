import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/example")
async def example():
    print(os.environ['TEST_SECRET'])
    return {"message": 'Hello'}
