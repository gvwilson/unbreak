from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/search")
def search(category: str):
    return {"category": category, "results": ["a", "b", "c"]}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
