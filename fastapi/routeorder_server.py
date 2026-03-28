from fastapi import FastAPI
import uvicorn

app = FastAPI()

ITEMS = {1: "apple", 2: "banana"}


# BUG: the parameterized route is registered first; FastAPI matches routes in
# BUG: declaration order, so the string "new" is captured as item_id and the
# BUG: /items/new route below is never reached; move /items/new above this route
@app.get("/items/{item_id}")
def get_item(item_id: str):
    return {"item_id": item_id, "matched": "parameterized route"}


@app.get("/items/new")
def new_item_form():
    return {"message": "ready to create a new item"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
