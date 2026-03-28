from fastapi import FastAPI
import uvicorn

app = FastAPI()


# BUG: counter is initialized to 0 inside the handler on every request;
# BUG: it always returns {"count": 1} instead of incrementing across calls;
# BUG: move counter = 0 to module level so it persists between requests
@app.get("/count")
def increment():
    counter = 0
    counter += 1
    return {"count": counter}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
