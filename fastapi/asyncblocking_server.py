import time

from fastapi import FastAPI
import uvicorn

app = FastAPI()


# BUG: time.sleep() is a blocking call; inside an async route it holds the GIL
# BUG: and freezes the entire event loop, so /fast cannot respond until /slow finishes
@app.get("/slow")
async def slow():
    time.sleep(2)
    return {"result": "done"}


@app.get("/fast")
async def fast():
    return {"result": "immediate"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
