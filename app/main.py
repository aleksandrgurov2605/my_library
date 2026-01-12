import time

from fastapi import FastAPI, Request

from app.logger import logger
from app.routers.books import books_router

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Логируем входящий запрос
    logger.info(f"Запрос: {request.method} {request.url.path}")

    response = await call_next(request)

    process_time = round(time.time() - start_time, 4)
    # Логируем результат
    logger.info(f"Ответ: {response.status_code} (время: {process_time} сек.)")

    return response

@app.get("/")
async def root():
    logger.debug("Это отладочное сообщение (не попадет в INFO)")
    return {"message": "Hello World"}


app.include_router(books_router)
