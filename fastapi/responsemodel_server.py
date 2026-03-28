from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class ItemIn(BaseModel):
    name: str
    price: float
    internal_code: str


# BUG: ItemOut does not include "internal_code"; FastAPI filters the
# BUG: response through response_model and silently drops the field,
# BUG: so the client never receives it even though the server has it
class ItemOut(BaseModel):
    name: str
    price: float


STORE: list[ItemIn] = []


@app.post("/items", response_model=ItemOut)
def create_item(item: ItemIn):
    STORE.append(item)
    return item


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
