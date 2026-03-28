from fastapi import FastAPI
import uvicorn

app = FastAPI()


# BUG: no status_code argument on the decorator, so FastAPI returns 200 by default;
# BUG: a POST that creates a resource should return 201 Created
@app.post("/items")
def create_item(name: str):
    return {"id": 1, "name": name}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
