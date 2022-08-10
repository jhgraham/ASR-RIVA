from fastapi import FastAPI

from .impl import RivaASRClient

app = FastAPI()

client = RivaASRClient()

@app.get("/")
async def root(file_path):

    print('path = ', file_path)

    return client.toText(file_path)

