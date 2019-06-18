from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse
from pydantic import BaseModel
import json
from redis_store import redis_load, redis_set
from worker import huey_model

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class StockName(BaseModel):
    name: str

def query_stock(stock:str) -> dict:
    redis_result = redis_load(stock)
    if not redis_result:
        redis_result = {"status": "processing"}
        redis_set(stock, redis_result)
        huey_model(stock)
    return redis_result

@app.get("/")
async def read_root():
    return templates.TemplateResponse('index.html', {'request': {}})


@app.post("/model")
async def model_route(item: StockName):
    """This route will return the results of a trained model if it exists or train a model if it doesn't"""
    result = query_stock(item.name)
    return JSONResponse(result)
