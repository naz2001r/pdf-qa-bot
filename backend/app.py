import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/example")
async def example():
    #print(os.environ['TEST_SECRET']) # now not in env var
    return {"message": 'Hello'}
