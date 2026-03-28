from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class Order(BaseModel):
    product: str
    quantity: int


@app.post("/orders")
def place_order(order: Order):
    return {"product": order.product, "quantity": order.quantity, "total": order.quantity * 5}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
