from fastapi import FastAPI, Query, Path, Body, Cookie, File, Form, Header, status, UploadFile, Request
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID
from datetime import datetime, timedelta, time
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing_extensions import Literal

app = FastAPI()


# @app.get('/')
# async def get_Root():
#     return {"message": "hey from get root"}
#
#
# @app.post('/')
# async def post_Root():
#     return {"message": "hey from post root"}
#
#
# @app.put('/')
# async def put_Root():
#     return {"message": "hey from put root"}
#
#
# @app.get('/users')
# async def users_list():
#     return {"message": "users list "}
#
#
# @app.get('/users/me')
# async def get_me_user():
#     return {"message": "specific endpoint caught before dynamic endpoint"}
#
#
# @app.get('/users/{user_id}')
# async def get_user(user_id: int):
#     return {"user_id": {user_id}}
#
#
# class FoodEnum(str, Enum):
#     fruit = "fruit"
#     meat = "meat"
#     milk = "milk"
#
#
# @app.get('/food/{food_name}')
# async def get_food(food_name: FoodEnum):
#     if food_name.value == FoodEnum.fruit:
#         return {"message": f"{food_name} is good"}
#     if food_name.value == FoodEnum.milk:
#         return {"message": f"{food_name} is tasty"}
#     return {"message": f"{food_name} is for kids"}
#
#
# # path + query params example:
# items = ["hat", "bike", "notebook", "pen"]
#
#
# @app.get('/items/{item_id}')
# async def get_item(item_id: int, q: str | None = None):
#     if q:
#         return {'item_id': f"{items[item_id]}", 'q': f"{q}"}
#     return {'item_id': f"{items[item_id]}"}
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#
# @app.post('/items')
# async def create_item(item: Item):
#     updated_price = item.price + item.price / 100 * item.tax
#     item_model = item.model_dump()
#     item_model.update({"updated_price": updated_price})
#     return item_model
#
#
# # an example of using Query() in order to enforce specific logic of the user's input
#
# @app.get('/items')
# async def read_items(q: str | None = Query(None, max_length=10, description="query string")):
#     # alias is a cool Query option used for giving another name to the query param.
#     # async def read_items(q: str = Query(..., min_length=2,max_length=10)):
#     # the 3 dots allow us to enforce a query param + not give it a default value
#     # async def read_items(q: list[str] | None = Query(None, max_length=10)):
#     # making q a list of values
#
#     if q:
#         return {"items": {"1": 'milk', "2": 'meat', 'q': q}}
#     return {"items": {"1": 'milk', "2": 'meat'}}
#
#
# @app.get('/items_validation/{item_id}')
# async def read_item_validation(
#         # astrix at the beginning makes all the parameters to be key value pairs
#         *,
#         item_id: int = Path(..., title='item id'),
#         q: str | None = Query(None, alias="item-query"),
#         b: str
#
# ):
#     result = {"item_id": item_id}
#     if q:
#         result.update({"q": q})
#     return result

# Example of using nested model:
#
# class Img(BaseModel):
#     url: HttpUrl
#     imgName: str
#
#
# class Item(BaseModel):
#     name: str = Field(..., example="foo")
#     price: float = Field(..., example=151)
#     tax: float | None = Field(None, example=3.54)
#     image: list[Img] | None = Field(None, example=["http://image_example.com", "http://images_for_example.com"])
#
#
# class Offer(BaseModel):
#     name: str
#     price: float
#     item: list[Item]
#
#
# @app.put('/offers')
# async def create_offer(
#         offer: Offer = Body(..., embed=True)
# ):
#     return offer
#
#
# async def read_items(
#         item_id: UUID,
#         start_date: datetime | None = Body(None),
#         end_date: datetime | None = Body(None),
#         repeat_at: time | None = Body(None),
#         process_after: timedelta | None = Body(None),
# ):
#     start_process = start_date + process_after
#     duration = end_date - start_process
#     return {
#         "item_id": item_id,
#         "start_date": start_date,
#         "end_date": end_date,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }
#
# @app.get("/items")
# async def read_items(
#     cookie_id: str | None = Cookie(None),
#     accept_encoding: str | None = Header(None),
#     sec_ch_ua: str | None = Header(None),
#     user_agent: str | None = Header(None),
#     x_token: list[str] | None = Header(None),
# ):
#     return {
#         "cookie_id": cookie_id,
#         "Accept-Encoding": accept_encoding,
#         "sec-ch-ua": sec_ch_ua,
#         "User-Agent": user_agent,
#         "X-Token values": x_token,
#     }
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float = 10.5
#     tags: list[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
#
# @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]
#
#
# @app.post("/items/", response_model=Item)
# async def create_item(item: Item):
#     return item
#
#
# class UserBase(BaseModel):
#     username: str
#     email: str
#     full_name: str | None = None
#
#
# class UserIn(UserBase):
#     password: str
#
#
# class UserOut(UserBase):
#     pass
#
#
# @app.post("/user/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserIn):
#     return user
#
#
# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include={"name", "description"},
# )
# async def read_item_name(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]
#
#
# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
# async def read_items_public_data(item_id: Literal["foo", "bar", "baz"]):
#     return items[item_id]


# Now let's say that the user want to send form-urlencoded instead of json. to handle it need to use Form
# The difference between the two methods is the format in which the data is sent.
#
# @app.post('/login/')
# async def login(username: str = Form(...), password: str = Form(...)):
#     print(password)
#     return {"username": username}
#
#
# @app.post('/login-json/')
# async def login(username: str = Body(...), password: str = Body(...)):
#     print(password)
#     return {"username": username}
#
#
# # uploading file like this:
#
# @app.post("/uploadfile/")
# async def create_upload_file(
#         files: list[UploadFile] = File(..., description="A file read as UploadFile")
# ):
#     return {"filename": [file.filename for file in files]}

### errors Handling

class myCustomeException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(myCustomeException)
async def my_exception_handler(request: Request, exc: myCustomeException):
    return JSONResponse(content={"message": "Ops my exception handler"}, status_code=418)


@app.get('/get_item/{item_id}')
def read_item(item_id: int):
    if item_id == 10:
        return HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="don't like 10")
    return {"item_id": item_id}


# can extend functionality StarletteHTTPException or

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"Omg! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/blah_items/{item_id}")
async def read_items(item_id: int):
    if item_id == 10:
        raise HTTPException(status_code=418, detail="Nope! I don't like 10.")
    return {"item_id": item_id}