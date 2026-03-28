from fastapi import FastAPI
import uvicorn

app = FastAPI()

ITEMS = {1: "apple", 2: "banana", 3: "cherry"}


# BUG: item_id is declared as str, but the dict keys are ints;
# BUG: str("3") != int(3), so every lookup returns "not found"
@app.get("/items/{item_id}")
def get_item(item_id: str):
    if item_id in ITEMS:
        return {"id": item_id, "name": ITEMS[item_id]}
    return {"error": "not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
