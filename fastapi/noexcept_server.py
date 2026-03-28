from fastapi import FastAPI
import uvicorn

app = FastAPI()

ITEMS = {1: "apple", 2: "banana"}


# BUG: when item_id is not in ITEMS, dict.get() returns None;
# BUG: FastAPI serializes None as a 200 response with body "null";
# BUG: raise HTTPException(status_code=404, detail="not found") instead
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return ITEMS.get(item_id)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
