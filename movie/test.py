# https://dev.to/paurakhsharma/microservice-in-python-using-fastapi-24cc
# FastAPI is a framework for creating APIs

# pip install fastapi
# pip install uvicorn  (Asynchronous Server Gateway Interface server)
# pip install 'databases[postgresql]'

# cd microservices
# uvicorn movie.test:app --reload --port 8080 >> http://127.0.0.1:8000 http://127.0.0.1:8000/docs

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

fake_movie_db = [
    {
        'name': 'Star Wars: Episode IX - The Rise of Skywalker',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver']
    }
]

class Movie(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[str]

# crud ops
@app.get('/', response_model=List[Movie])
async def index():
    return fake_movie_db

@app.post('/', status_code=201)
async def add_movie(payload: Movie):
    movie = payload.dict()
    fake_movie_db.append(movie)
    return {'id': len(fake_movie_db) - 1}

@app.put('/{id}')
async def update_movie(id: int, payload: Movie):
    movie = payload.dict()
    movies_length = len(fake_movie_db)
    if 0 <= id <= movies_length:
        raise HTTPException(status_code=404, detail="Movie with given id not found")
    fake_movie_db[id] = movie
    return None

@app.delete('/{id}')
async def delete_movie(id: int):
    movies_length = len(fake_movie_db)
    if 0 <= id <= movies_length:
        raise HTTPException(status_code=404, detail="Movie with given id not found")
    del fake_movie_db[id]
    return None
