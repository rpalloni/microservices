# service postgresql start
# cd microservices
# uvicorn movie.test:app --reload --port 8080

from fastapi import FastAPI
from movie.api.movies import movies
from movie.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(movies)
