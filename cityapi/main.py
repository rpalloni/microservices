# https://www.youtube.com/watch?v=kCggyi_7pHg
# http://worldtimeapi.org/

# cd microservices
# uvicorn cityapi.main:app --reload --port 8080
# >> http://127.0.0.1:8080 http://127.0.0.1:8080/docs http://127.0.0.1:8080/redoc

import requests
from fastapi import FastAPI
from pydantic import BaseModel # create a data structure (model) for the city

app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: str


@app.get('/')
def index():
    return {'key':'value'}


# endpoints for crud ops
@app.get('/cities')
def get_cities():
    results = []
    for city in db:
        r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}') # http://worldtimeapi.org/api/timezone
        current_time = r.json()['datetime']
        results.append({'name':city['name'],
                        'timezone':city['timezone'],
                        'current_time':current_time})
    return results

@app.get('/cities/{city_id}')
def get_cities(city_id: int):
    return db[city_id]

@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1] # return last created

'''
{
  "name": "Rome",
  "timezone": "Europe/Rome"
}
'''

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id)
    return {}
