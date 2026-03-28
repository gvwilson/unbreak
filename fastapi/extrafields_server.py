from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float = 0.0


@app.post("/items")
def create_item(item: Item):
    return {"received": item.model_dump()}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
