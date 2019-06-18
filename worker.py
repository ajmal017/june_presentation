from huey import RedisHuey
from prophet_model import train_model
from redis_store import redis_set

huey = RedisHuey()

@huey.task()
def huey_model(stock: str):
    result = train_model(stock)
    result = {"status": "done", "cv": result.cv, "forecast": result.forecast}
    redis_set(stock, result)
