from fastapi import FastAPI, Query
from enum import Enum
from pydantic import BaseModel

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


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post('/items')
async def create_item(item: Item):
    updated_price = item.price + item.price / 100 * item.tax
    item_model = item.model_dump()
    item_model.update({"updated_price": updated_price})
    return item_model




# an example of using Query() in order to enforce specific logic of the user's input

@app.get('/items')
async def read_items(q: str | None = Query(None, max_length=10,description="query string")):
    #alias is a cool Query option used for giving another name to the query param.
    # async def read_items(q: str = Query(..., min_length=2,max_length=10)):
    # the 3 dots allow us to enforce a query param + not give it a default value
    # async def read_items(q: list[str] | None = Query(None, max_length=10)):
    # making q a list of values

    if q:
        return {"items": {"1": 'milk', "2": 'meat', 'q': q}}
    return {"items": {"1": 'milk', "2": 'meat'}}
