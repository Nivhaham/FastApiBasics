from fastapi import FastAPI
from enum import Enum

app = FastAPI()


@app.get('/')
async def get_Root():
    return {"message": "hey from get root"}


@app.post('/')
async def post_Root():
    return {"message": "hey from post root"}


@app.put('/')
async def put_Root():
    return {"message": "hey from put root"}


@app.get('/users')
async def users_list():
    return {"message": "users list "}


@app.get('/users/me')
async def get_me_user():
    return {"message": "specific endpoint caught before dynamic endpoint"}


@app.get('/users/{user_id}')
async def get_user(user_id: int):
    return {"user_id": {user_id}}


class FoodEnum(str, Enum):
    fruit = "fruit"
    meat = "meat"
    milk = "milk"


@app.get('/food/{food_name}')
async def get_food(food_name: FoodEnum):
    if food_name.value == FoodEnum.fruit:
        return {"message": f"{food_name} is good"}
    if food_name.value == FoodEnum.milk:
        return {"message": f"{food_name} is tasty"}
    return {"message": f"{food_name} is for kids"}


# path + query params example:
items = ["hat", "bike", "notebook", "pen"]


@app.get('/items/{item_id}')
async def get_item(item_id: int, q: str | None = None):
    if q:
        return {'item_id': f"{items[item_id]}", 'q': f"{q}"}
    return {'item_id': f"{items[item_id]}"}
