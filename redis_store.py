from redis import Redis
import json

r = Redis()
r.flushdb()

def redis_set(stock: str, value: dict):
    r.set(stock, json.dumps(value))

def redis_load(stock: str) -> dict:
    result = r.get(stock)
    if type(result) is bytes:
        result = json.loads(result.decode('utf-8'))
    return result