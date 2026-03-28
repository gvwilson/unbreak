from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Item(BaseModel):
    name: str = ""
    price: float = 0.0
    in_stock: bool = True


STORE: dict[int, Item] = {1: Item(name="widget", price=9.99, in_stock=True)}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = STORE.get(item_id)
    return item if item else {"error": "not found"}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    STORE[item_id] = item
    return STORE[item_id]


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
