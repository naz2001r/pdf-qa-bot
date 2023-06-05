import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/data")
async def root():
    return {"message": os.listdir('/data')}